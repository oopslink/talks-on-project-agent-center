#!/usr/bin/env python3
"""Build static data for docs/ from data/talks/ channel JSON files."""

import json
import os
import shutil
import glob
from collections import defaultdict
from datetime import datetime, timezone

TALKS_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'talks')
DOCS_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'docs', 'data')
CHANNELS_DIR = os.path.join(DOCS_DATA_DIR, 'channels')


def build():
    os.makedirs(CHANNELS_DIR, exist_ok=True)

    # Load all channels
    all_channels = {}
    for path in sorted(glob.glob(os.path.join(TALKS_DIR, 'channel-*.json'))):
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        all_channels[data['channelId']] = data

    print(f'Loaded {len(all_channels)} channel files')

    # Find root channels (channelIds NOT appearing as any message's threadId)
    all_thread_ids = set()
    for ch in all_channels.values():
        for msg in ch['messages']:
            if msg.get('threadId'):
                all_thread_ids.add(msg['threadId'])

    root_ids = set(all_channels.keys()) - all_thread_ids
    print(f'Root channels: {len(root_ids)}, Thread channels: {len(all_channels) - len(root_ids)}')

    # Build root -> threads mapping (order by first occurrence in root messages)
    root_to_threads = {rid: [] for rid in root_ids}
    thread_to_root = {}
    for rid in root_ids:
        ch = all_channels[rid]
        seen = set()
        for msg in ch['messages']:
            tid = msg.get('threadId')
            if tid and tid not in seen:
                seen.add(tid)
                root_to_threads[rid].append(tid)
                thread_to_root[tid] = rid

    # Global stats aggregated across all channels
    task_counts = defaultdict(int)
    heatmap = [[0] * 24 for _ in range(7)]   # [dayOfWeek 0=Mon][hour 0-23]
    daily_counts = defaultdict(int)
    sender_map = {}   # senderId -> {name, type, count}

    for ch in all_channels.values():
        for msg in ch['messages']:
            status = msg.get('taskStatus')
            if status:
                task_counts[status] += 1

            ts = msg.get('createdAt', '')
            if ts:
                try:
                    dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                    heatmap[dt.weekday()][dt.hour] += 1
                    daily_counts[dt.strftime('%Y-%m-%d')] += 1
                except ValueError:
                    pass

            sid = msg.get('senderId', '')
            if sid:
                if sid not in sender_map:
                    sender_map[sid] = {
                        'name': msg.get('senderName', ''),
                        'type': msg.get('senderType', 'user'),
                        'count': 0,
                    }
                sender_map[sid]['count'] += 1

    total_messages = sum(len(ch['messages']) for ch in all_channels.values())

    top_senders = sorted(
        [{'name': v['name'], 'type': v['type'], 'count': v['count']}
         for v in sender_map.values()],
        key=lambda x: -x['count']
    )[:10]

    daily_activity = [
        {'date': d, 'count': c}
        for d, c in sorted(daily_counts.items())[-60:]
    ]

    # Build per-channel summary objects
    def make_label(ch_data):
        """Derive a short display label from the first chat message."""
        for msg in ch_data['messages']:
            content = (msg.get('content') or '').strip()
            if content and msg.get('messageType') == 'chat':
                # Strip @mentions at start, trim to 24 chars
                text = content.lstrip('@').split('\n')[0]
                return text[:24]
        return ch_data['channelId'][:8]

    channel_summaries = []
    for cid, ch in all_channels.items():
        msgs = ch['messages']
        first_content = ''
        created_at = ''
        for msg in msgs:
            c = (msg.get('content') or '').strip()
            if c and msg.get('messageType') == 'chat':
                first_content = c[:120]
                created_at = msg.get('createdAt', '')
                break

        summary = {
            'channelId': cid,
            'total': len(msgs),
            'label': make_label(ch),
            'firstMessage': first_content,
            'createdAt': created_at,
        }
        if cid in root_ids:
            summary['type'] = 'root'
            summary['threadIds'] = root_to_threads[cid]
        else:
            summary['type'] = 'thread'
            summary['rootChannelId'] = thread_to_root.get(cid, '')
        channel_summaries.append(summary)

    # Write index.json
    index = {
        'generatedAt': datetime.now(timezone.utc).isoformat(),
        'stats': {
            'totalMessages': total_messages,
            'totalChannels': len(all_channels),
            'rootChannels': len(root_ids),
            'threadChannels': len(all_channels) - len(root_ids),
            'uniqueSenders': len(sender_map),
            'taskCounts': dict(task_counts),
            'heatmap': heatmap,
            'topSenders': top_senders,
            'dailyActivity': daily_activity,
        },
        'channels': channel_summaries,
    }
    out = os.path.join(DOCS_DATA_DIR, 'index.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, separators=(',', ':'))
    print(f'Wrote {out}  ({os.path.getsize(out) // 1024} KB)')

    # Write search.json — flat list of all non-empty messages
    search_entries = []
    for ch in all_channels.values():
        for msg in ch['messages']:
            content = (msg.get('content') or '').strip()
            if not content:
                continue
            search_entries.append({
                'channelId': msg['channelId'],
                'msgId': msg['id'],
                'senderName': msg.get('senderName', ''),
                'senderType': msg.get('senderType', 'user'),
                'content': content[:200],
                'createdAt': msg.get('createdAt', ''),
            })
    out = os.path.join(DOCS_DATA_DIR, 'search.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(search_entries, f, ensure_ascii=False, separators=(',', ':'))
    print(f'Wrote {out}  ({os.path.getsize(out) // 1024} KB, {len(search_entries)} entries)')

    # Copy individual channel files
    for cid in all_channels:
        src = os.path.join(TALKS_DIR, f'channel-{cid}.json')
        dst = os.path.join(CHANNELS_DIR, f'{cid}.json')
        shutil.copy2(src, dst)
    print(f'Copied {len(all_channels)} channel files to {CHANNELS_DIR}')


if __name__ == '__main__':
    build()
