#!/usr/bin/env python3
"""
Extract keyword-based semantic links between cross-root thread channels.

For each thread, we:
1. Collect all message text (first N chars each to keep it fast)
2. Extract English technical terms: CamelCase, snake_case, kebab-case, file paths, identifiers
3. Extract Chinese technical bigrams/trigrams that appear >=2 times in a thread
4. Compute Jaccard similarity between cross-root thread keyword sets
5. Output pairs above threshold as semantic links

Output: docs/data/semantic_links.json
"""

import json
import os
import re
import glob
from collections import Counter, defaultdict

TALKS_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'talks')
DOCS_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'docs', 'data')

# Tune these
MAX_MSG_CHARS = 300     # chars per message to consider
MAX_MSGS_PER_THREAD = 80
JACCARD_THRESHOLD = 0.06   # min Jaccard similarity to emit a semantic link
MAX_LINKS_PER_THREAD = 5   # cap to avoid over-cluttering
MIN_KEYWORDS = 4           # skip threads with too few keywords

# Chinese characters range
ZH_RE = re.compile(r'[\u4e00-\u9fff]')

# English technical term patterns
EN_CAMEL = re.compile(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b')          # CamelCase
EN_SNAKE = re.compile(r'\b[a-z][a-z0-9]*(?:_[a-z0-9]+){1,}\b')     # snake_case
EN_KEBAB = re.compile(r'\b[a-z][a-z0-9]*(?:-[a-z0-9]+){1,}\b')     # kebab-case
EN_PATH  = re.compile(r'[a-zA-Z0-9_\-]+(?:/[a-zA-Z0-9_\-]+){1,}')  # path/like/this
EN_IDENT = re.compile(r'\b[a-zA-Z][a-zA-Z0-9]{3,}\b')              # plain identifiers ≥4 chars

# Common stopwords to exclude
EN_STOP = {
    # generic English
    'this', 'that', 'with', 'from', 'have', 'been', 'will', 'would', 'could',
    'should', 'there', 'their', 'about', 'when', 'then', 'what', 'which',
    'some', 'more', 'also', 'into', 'your', 'just', 'each', 'very',
    'true', 'false', 'null', 'none', 'self', 'return', 'string', 'number',
    'error', 'value', 'type', 'name', 'data', 'item', 'list', 'make',
    'done', 'note', 'code', 'test', 'file', 'func', 'args', 'opts',
    'todo', 'fixme', 'hack', 'user', 'agent', 'bool', 'byte', 'time',
    # project-wide noise (appear in nearly every thread)
    'task', 'center', 'main', 'commit', 'origin', 'push', 'merge', 'open',
    'project', 'release', 'branch', 'state', 'status', 'build', 'docs',
    'delete', 'detail', 'config', 'issue', 'issues', 'channel', 'mention',
    'moved', 'locked', 'install', 'message', 'context', 'result', 'output',
    'request', 'response', 'update', 'check', 'start', 'close', 'create',
    # project-specific actor names (appear in every thread)
    'oopslink', 'agentcenterdev', 'agentcenterpd', 'agentcentertester',
    'agentcenterdev2', 'integrationdev', 'tester', 'acceptance',
    # git noise
    'remote', 'fetch', 'clone', 'rebase', 'stash', 'diff', 'staged',
    'shipped', 'hotfix', 'patch',
}

ZH_STOP_CHARS = set('的了在是我你他她我们你们他们的地得和与或但是因为所以而且还有这那个一二三四五六七八九十')


def extract_keywords(text: str) -> set[str]:
    """Extract technical keyword tokens from a mixed Chinese/English text."""
    keywords = set()

    # English technical terms
    for pat in [EN_CAMEL, EN_SNAKE, EN_KEBAB, EN_PATH]:
        for m in pat.finditer(text):
            w = m.group().lower()
            if w not in EN_STOP:
                keywords.add(w)

    # Plain English identifiers ≥4 chars, not stopwords
    for m in EN_IDENT.finditer(text):
        w = m.group().lower()
        if w not in EN_STOP and not w.isdigit():
            keywords.add(w)

    # Chinese bigrams + trigrams (sliding window)
    zh_chars = [c for c in text if ZH_RE.match(c) and c not in ZH_STOP_CHARS]
    # Count bigrams
    bigram_count: Counter = Counter()
    for i in range(len(zh_chars) - 1):
        bigram_count[zh_chars[i] + zh_chars[i+1]] += 1
    # Keep bigrams appearing ≥2 times (likely meaningful phrases)
    for bg, cnt in bigram_count.items():
        if cnt >= 2:
            keywords.add(bg)

    # Count trigrams
    trigram_count: Counter = Counter()
    for i in range(len(zh_chars) - 2):
        trigram_count[zh_chars[i] + zh_chars[i+1] + zh_chars[i+2]] += 1
    for tg, cnt in trigram_count.items():
        if cnt >= 2:
            keywords.add(tg)

    return keywords


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def build_semantic_links():
    # Load all channels
    all_channels: dict = {}
    for path in sorted(glob.glob(os.path.join(TALKS_DIR, 'channel-*.json'))):
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        all_channels[data['channelId']] = data

    print(f'Loaded {len(all_channels)} channel files')

    # Identify roots vs threads
    all_thread_ids: set[str] = set()
    for ch in all_channels.values():
        for msg in ch['messages']:
            if msg.get('threadId'):
                all_thread_ids.add(msg['threadId'])

    root_ids = set(all_channels.keys()) - all_thread_ids
    thread_to_root: dict[str, str] = {}
    for rid in root_ids:
        for msg in all_channels[rid]['messages']:
            tid = msg.get('threadId')
            if tid and tid not in thread_to_root:
                thread_to_root[tid] = rid

    threads_only = {cid: ch for cid, ch in all_channels.items() if cid in all_thread_ids}
    print(f'Processing {len(threads_only)} thread channels for keywords')

    # Build keyword sets per thread
    thread_keywords: dict[str, set[str]] = {}
    for cid, ch in threads_only.items():
        texts = []
        for msg in ch['messages'][:MAX_MSGS_PER_THREAD]:
            content = (msg.get('content') or '').strip()
            if content:
                texts.append(content[:MAX_MSG_CHARS])
        combined = ' '.join(texts)
        kw = extract_keywords(combined)
        if len(kw) >= MIN_KEYWORDS:
            thread_keywords[cid] = kw

    print(f'Built keyword sets for {len(thread_keywords)} threads (≥{MIN_KEYWORDS} keywords)')

    # Get threads grouped by root
    root_list = list(root_ids)
    threads_by_root: dict[str, list[str]] = defaultdict(list)
    for tid in thread_keywords:
        rid = thread_to_root.get(tid)
        if rid:
            threads_by_root[rid].append(tid)

    if len(root_list) < 2:
        print('Only 1 root channel, no cross-root links possible')
        return []

    # Find cross-root pairs above threshold
    # To avoid O(n^2) with 489 threads, group by root and only compare cross-root
    roots = list(threads_by_root.keys())
    all_links = []

    for i, root_a in enumerate(roots):
        for j, root_b in enumerate(roots):
            if j <= i:
                continue
            threads_a = threads_by_root[root_a]
            threads_b = threads_by_root[root_b]
            pairs = []
            for ta in threads_a:
                kw_a = thread_keywords[ta]
                for tb in threads_b:
                    kw_b = thread_keywords[tb]
                    sim = jaccard(kw_a, kw_b)
                    if sim >= JACCARD_THRESHOLD:
                        shared = sorted(kw_a & kw_b)
                        pairs.append({
                            'source': ta,
                            'target': tb,
                            'weight': round(sim, 3),
                            'tags': shared[:8],
                        })

            # Sort by weight desc, cap total
            pairs.sort(key=lambda x: -x['weight'])
            all_links.extend(pairs)

    print(f'Found {len(all_links)} cross-root semantic link candidates')

    # Cap per-thread: each thread gets at most MAX_LINKS_PER_THREAD outgoing links
    link_count: Counter = Counter()
    final_links = []
    all_links.sort(key=lambda x: -x['weight'])
    for lnk in all_links:
        sa, sb = lnk['source'], lnk['target']
        if link_count[sa] < MAX_LINKS_PER_THREAD and link_count[sb] < MAX_LINKS_PER_THREAD:
            final_links.append(lnk)
            link_count[sa] += 1
            link_count[sb] += 1

    print(f'After per-thread cap ({MAX_LINKS_PER_THREAD}): {len(final_links)} links')

    # Write output
    out_path = os.path.join(DOCS_DATA_DIR, 'semantic_links.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(final_links, f, ensure_ascii=False, separators=(',', ':'))
    size_kb = os.path.getsize(out_path) // 1024
    print(f'Wrote {out_path}  ({size_kb} KB, {len(final_links)} links)')

    # Print top 10 for inspection
    print('\nTop 10 semantic links by weight:')
    for lnk in final_links[:10]:
        sa, sb = lnk['source'][:8], lnk['target'][:8]
        print(f'  {sa} <-> {sb}  weight={lnk["weight"]}  tags={lnk["tags"][:5]}')

    return final_links


if __name__ == '__main__':
    build_semantic_links()
