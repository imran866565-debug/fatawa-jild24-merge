#!/usr/bin/env python3
"""Merge Jild 24 tashreeh chunks into jild-24.json.

Re-runnable: reads every jild-24-chunk-*.json listed in the manifest,
merges in chunk order, validates (unique ids, page coverage, empty
jawab allow-list), writes jild-24.json, and updates the manifest statuses.

INPUT (verified on disk by the parent):
  17 chunk files (chunk 11 split into 11a/11b), 211 chunk items,
  volume_id 39. Source export ~/workspace/fatawa-app/content/jild-24.json:
  640 unique pages pp. 6-720. Gaps (75, nothing invented): pp. 12-75
  (64), 167, 177, 285, 287, 367, 453, 461, 531, 573, 679, 711 — every
  gap listed in each chunk's manifest missing_pages (Jild 17 lesson),
  except pp. 167 and 285 which lie BETWEEN chunks (167 between chunk
  02 end p. 166 and chunk 03 start p. 168; 285 between chunk 05 end
  p. 284 and chunk 06 start p. 286) and are inside NO chunk's span.
  Validate against the chunk items' page union (640 pages), NOT
  range arithmetic.

COMBINE RULES (4 cases; parts ordered by min page; pages = UNION of
all parts' pages; notes = all parts' notes; start_page = min page):
  masala 18:   SAME-ID, sawal CONCATENATED (Jild 12 masala-289
               precedent). Chunk 01 [120] (sawal 1,677, jawab EMPTY)
               + chunk 02 [121-125] (sawal 1,473, jawab 5,382) ->
               [120-125]. Chunk 02's sawal covers ONLY the question
               tail on p. 121 (stated in its item note) and must be
               concatenated after chunk 01's sawal -> merged sawal
               3,150 chars, jawab 5,382.
  masala 84:   CROSS-ID, rename-then-combine (Jild 16 masala-83-87
               precedent). Chunk 04 'jild24-masala-84' [216-250]
               (sawal 539, jawab 37,440) + chunk 05
               'jild24-risala-139' [251-284] (empty sawal, jawab
               33,838) -> ONE item 'jild24-masala-84', pages
               [216-284] (69 pages). Sawal from chunk 04; jawab
               concatenated (37,440 + 33,838 = 71,278). The rename
               of the tail item is effected by the combine itself
               (the tail id is absorbed; the result keeps the head
               id). Risala 139 (الحق المجتلیٰ فی حکم المبتلٰی) is ONE
               mas'ala (84); ends p. 284 "ختم ہوا".
  masala 166:  SAME-ID, keep first half's sawal (Jild 11 masala-16
               rule). Chunk 08 [416-417] (sawal 2,019, jawab EMPTY)
               + chunk 09 [418-450] (empty sawal, jawab 16,733) ->
               [416-450]. Sawal 2,019, jawab 16,733. The id was
               inferred by chunk 09 from the next mas'ala being 167
               on p. 451; chunk 08's printed heading CONFIRMED 166,
               so no rename. Note: p. 450 answer ends mid-sentence
               in the source (risala 146's closing words missing
               from the source DB).
  masala 250:  SAME-ID, keep first half's sawal, jawabs concatenated.
               Chunk 13 [571-600] (gap p. 573 inside; sawal 907,
               jawab 33,294) + chunk 14 [601-643] (empty sawal,
               jawab 49,812) -> [571-643] minus 573. Sawal 907,
               jawab 83,106. Risala 155 (العطایا القدیر فی حکم
               التصویر ۱۳۳۱ھ) is ONE mas'ala (250); ends p. 643
               "ختم ہوا".
After all 4 combines: 211 - 4 = 207 items covering 640 unique pages.

RENAMES: one merge-time rename inside combine 2 above
('jild24-risala-139' -> 'jild24-masala-84'), effected by the combine
itself (the tail id is absorbed; the result keeps the head id). One
rename was already applied in the chunk files and must NOT be
re-applied: printed 279 (p. 669) -> 'jild24-masala-269' [669-670]
(chunk 15; the item's note records the print error; sequence 268
[666-669] -> 270-272 [670-671] proves 269). Do NOT globally
normalise bare ids.

CORRECTION (parent-verified, the coordinator's report got this
wrong): the coordinator wrote "No other item claims 279" — FALSE. A
DIFFERENT, genuine 'jild24-masala-279' exists in chunk 16, pages
[709, 710, 712, 713, 714], title "مسئلہ ۲۷۹ — بلا اجازت کسی کا خط
روکنا، کھولنا اور پڑھنا", sawal 2,114 chars, jawab 4,140 chars. It
is a separate mas'ala on entirely different pages from the renamed
masala-269 [669-670]. Do NOT rename it, do NOT merge it with
masala-269, do NOT treat it as a duplicate. The merged file must
contain BOTH 'jild24-masala-269' [669-670] AND 'jild24-masala-279'
[709, 710, 712, 713, 714] as separate items.

EMPTY-JAWAB ALLOW-LIST: after the combines, exactly ONE item has an
empty tashreeh_jawab: 'jild24-masala-64' [196] (sawal 112 chars,
jawab EMPTY). The parent verified this from the source export
itself: p. 196 ends with "مسئلہ ۶۴: ... شفاخانہ کی دوا استعمال کرنے
کاکیاحکم ہے؟\nالجواب:\n" — the question is followed by a bare
«الجواب:» with no answer text, and p. 197 opens directly into
masala-65's text. It is genuinely empty in the source, NOT a
translator omission. The merge script allow-lists exactly this one
item. All other items must have non-empty jawab (the two split-head
empty jawabs — masala-18 [120], masala-166 [416-417] — are resolved
by combines 1 and 3). Empty sawal after merge: only pesh-lafz
(by design).

DO-NOT-COMBINES: chunk 11 was split into 11a/11b after a translator
failure; NO mas'ala spans the 489/490 boundary. Absent numbers, NOT
misprints — do NOT renumber: masala-69 (numbering jumps 68->70,
chunk 03); masala-141 (jumps 140->142, chunk 07). Grouped items
kept as single items under the FIRST number's plain id (not a range
id): masala-117 [347-350] (title "مسئلہ ۱۱۷ تا ۱۲۰"), masala-130
[361-363] (title "مسئلہ ۱۳۰ تا ۱۳۵"), masala-143 [372-373],
masala-146 [373], masala-148 [374], masala-151 [379-380],
masala-153 [380-381]; and range ids masala-4-12 [87-111], 25-27,
39-41, 42-46, 85-93, 169-171, 175-178, 182-183, 187-191, 197-203,
207-219, 230-232, 237-241. Shared pages by design (one mas'ala
ends, the next begins on the same page). Page union must still be
exactly 640. Volume ends p. 720 with the closing note «جلد ۲۴
سیاسیات کے عنوان پر ختم ہوئی، جلد ۲۵ ان شاء اللہ کتاب المدانیات سے
شروع ہوگی» recorded in masala-284's notes. Last item
'jild24-masala-284' [719-720]. PUA-garbled Quran pages: 5 — p. 162
(chunk 02, masala-42-46), p. 341 (chunk 07, masala-111), p. 419
(chunk 09, masala-166), p. 432 (chunk 09, masala-166), p. 705
(chunk 16, masala-278). Flagged in item notes only, never
reconstructed. No U+FFFD pages.

SORT: merged items are sorted by start_page for the final file.
"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))

# result id -> list of selectors, in page order.
# Selector forms:
#   ('id', sid)            — every item with this id (1 or 2 halves)
#   ('id_start', sid, sp)  — the item with this id starting at page sp
COMBINES = {
    'jild24-masala-18': [
        ('id', 'jild24-masala-18'),
    ],
    'jild24-masala-84': [
        ('id', 'jild24-masala-84'),
        ('id', 'jild24-risala-139'),
    ],
    'jild24-masala-166': [
        ('id', 'jild24-masala-166'),
    ],
    'jild24-masala-250': [
        ('id', 'jild24-masala-250'),
    ],
}

# Sawal handling per combined id (default: sawal from the first part).
# masala-18 is the ONLY combine whose sawal is concatenated from both
# halves (Jild 12 masala-289 precedent: chunk 02's sawal is the
# question tail on p. 121 only).
SAWAL_RULES = {
    'jild24-masala-18': ('concat', [0, 1]),
}

# No renames to apply as a separate step — the one merge-time rename
# (risala-139 -> masala-84) is effected by the cross-id combine
# itself (the tail id is absorbed; the result keeps the head id), and
# the applied-in-chunk rename (printed 279 -> masala-269) is already
# in the chunk files and is asserted present below. Kept empty
# deliberately.
RENAMES = {}

# Applied-in-chunk renames (already in the chunk files — must exist
# after merging, never re-applied).
RENAMED_IN_CHUNK = ['jild24-masala-269']

# Expected pages for every combined item (spot-check anchors).
EXPECTED_COMBINED_PAGES = {
    'jild24-masala-18': [120, 121, 122, 123, 124, 125],
    'jild24-masala-84': list(range(216, 285)),
    'jild24-masala-166': list(range(416, 451)),
    # gap p. 573 inside the head half
    'jild24-masala-250': [571, 572] + list(range(574, 644)),
}

# Expected sawal/jawab char counts for every combined item.
# masala-18 sawal: 1677 + 1473 = 3150; jawab: 0 + 5382 = 5382
# masala-84 jawab: 37440 + 33838 = 71278
# masala-166 jawab: 0 + 16733 = 16733
# masala-250 jawab: 33294 + 49812 = 83106
EXPECTED_COMBINED_TEXT = {
    'jild24-masala-18': (3150, 5382),
    'jild24-masala-84': (539, 71278),
    'jild24-masala-166': (2019, 16733),
    'jild24-masala-250': (907, 83106),
}

# The only ids that may be absorbed by a combine (must be gone after).
ABSORBED = ['jild24-risala-139']

# The only items allowed to keep an empty sawal after merging.
EMPTY_SAWAL_ALLOWED = {'jild24-pesh-lafz'}

# The ONLY item allowed to keep an empty tashreeh_jawab after merging:
# genuinely empty in the source (bare «الجواب:» at the end of p. 196;
# p. 197 opens masala-65). Verified by the parent from the source
# export. Every other item must have a non-empty jawab.
EMPTY_JAWAB_ALLOWED = {'jild24-masala-64'}

# Both 269 and 279 must exist as SEPARATE items (see CORRECTION in
# the docstring above): the renamed masala-269 [669-670] and the
# genuine masala-279 [709, 710, 712, 713, 714].
BOTH_269_AND_279 = {
    'jild24-masala-269': [669, 670],
    'jild24-masala-279': [709, 710, 712, 713, 714],
}


def combine_parts(result_id, parts):
    parts = sorted(parts, key=lambda it: min(it['pages']))
    first = parts[0]
    rule = SAWAL_RULES.get(result_id)
    if rule and rule[0] == 'concat':
        sawal = ''.join((parts[i].get('tashreeh_sawal', '') or '')
                        for i in rule[1])
    elif rule and rule[0] == 'from':
        sawal = parts[rule[1]].get('tashreeh_sawal', '') or ''
    else:
        sawal = first.get('tashreeh_sawal', '') or ''
    title = first.get('title') or ''
    combined = {
        'id': result_id,
        'title': title,
        'volume_id': 39,
        'pages': sorted(set().union(*[set(p['pages']) for p in parts])),
        'start_page': min(min(p['pages']) for p in parts),
        'tashreeh_sawal': sawal,
        'tashreeh_jawab': ''.join((p.get('tashreeh_jawab', '') or '') for p in parts),
        'notes': [n for p in parts for n in (p.get('notes') or [])],
    }
    return combined


def select_parts(all_items, selectors):
    """Resolve selectors to the matching items (each used at most once)."""
    parts = []
    used = set()
    for sel in selectors:
        if sel[0] == 'id':
            hits = [it for it in all_items
                    if it['id'] == sel[1] and id(it) not in used]
        elif sel[0] == 'id_start':
            hits = [it for it in all_items
                    if it['id'] == sel[1] and it['start_page'] == sel[2]
                    and id(it) not in used]
        else:
            raise ValueError(f'unknown selector {sel}')
        assert hits, f'no items matched selector {sel}'
        for it in hits:
            used.add(id(it))
        parts.extend(hits)
    return parts


def run_merge(manifest_path, base, write=False):
    manifest = json.load(open(manifest_path, encoding='utf-8'))
    all_items = []
    merged_chunks = []
    for entry in manifest['chunks']:
        nn = entry['chunk']
        if entry.get('status') == 'split-halves':
            print(f'chunk {nn}: split-halves placeholder — halves are separate entries, skipping')
            continue
        # A chunk may be one file ("file") or split halves ("files").
        file_list = entry.get('files') or [entry['file']]
        items = []
        for fname in file_list:
            path = os.path.join(base, fname)
            if not os.path.exists(path):
                print(f'chunk {nn}: {fname} not yet written')
                continue
            try:
                d = json.load(open(path, encoding='utf-8'))
            except json.JSONDecodeError as e:
                # File may still be streaming from its translator; skip it
                # for now instead of crashing the whole merge.
                print(f'chunk {nn}: {fname} not valid JSON yet ({e}) — skipping for now')
                continue
            items.extend(d['masail'])
        if not items:
            print(f'chunk {nn}: no items loaded — skipping')
            continue
        # Normalize: some translators omit start_page; derive it from pages.
        for it in items:
            if 'start_page' not in it:
                assert it.get('pages'), f'chunk {nn} item {it.get("id")} has no pages'
                it['start_page'] = it['pages'][0]
                print(f'chunk {nn}: derived start_page={it["start_page"]} for {it["id"]}')
            assert it['start_page'] == min(it['pages']), \
                f'chunk {nn} item {it["id"]}: start_page != first page'
            it['_src_file'] = file_list[0]
        all_items.extend(items)
        merged_chunks.append(nn)
        entry['status'] = 'merged'
        print(f'chunk {nn}: {len(items)} items merged')
    print(f'items before combines: {len(all_items)}')
    assert len(all_items) == 211, f'expected 211 chunk items, got {len(all_items)}'
    # COMBINE the 4 cases (one mas'ala split across chunks).
    for result_id, selectors in COMBINES.items():
        parts = select_parts(all_items, selectors)
        combined = combine_parts(result_id, parts)
        assert combined['pages'] == EXPECTED_COMBINED_PAGES[result_id], \
            f'{result_id}: pages {combined["pages"]} != expected {EXPECTED_COMBINED_PAGES[result_id]}'
        exp_sawal, exp_jawab = EXPECTED_COMBINED_TEXT[result_id]
        assert len(combined['tashreeh_sawal']) == exp_sawal, \
            f'{result_id}: sawal {len(combined["tashreeh_sawal"])} chars != expected {exp_sawal}'
        assert len(combined['tashreeh_jawab']) == exp_jawab, \
            f'{result_id}: jawab {len(combined["tashreeh_jawab"])} chars != expected {exp_jawab}'
        assert combined['tashreeh_jawab'], f'{result_id}: combined jawab is empty!'
        assert combined['tashreeh_sawal'], f'{result_id}: combined sawal is empty!'
        assert combined['start_page'] == min(combined['pages']), f'{result_id}: start_page != min(pages)'
        used_ids = set(id(p) for p in parts)
        all_items = [it for it in all_items if id(it) not in used_ids]
        all_items.append(combined)
        print(f'COMBINED {result_id}: {len(parts)} parts, pages {combined["pages"][0]}-{combined["pages"][-1]} '
              f'({len(combined["pages"])} pages), sawal {len(combined["tashreeh_sawal"])} chars, '
              f'jawab {len(combined["tashreeh_jawab"])} chars, notes {len(combined["notes"])}')
    # RENAMES: none to apply as a separate step (the merge-time rename
    # was effected by the cross-id combine above).
    for old_id, new_id in RENAMES.items():
        assert not any(it['id'] == new_id for it in all_items), \
            f'rename target {new_id} already exists!'
        hits = [it for it in all_items if it['id'] == old_id]
        assert len(hits) == 1, f'rename source {old_id}: expected exactly 1 item, found {len(hits)}'
        hits[0]['id'] = new_id
        print(f'RENAMED {old_id} -> {new_id} (pages {hits[0]["pages"][0]}-{hits[0]["pages"][-1]})')
    # Verify absorbed ids are gone.
    for sid in ABSORBED:
        assert not any(it['id'] == sid for it in all_items), \
            f'absorbed id {sid} must not exist after combining!'
    print(f'absorbed ids gone: {ABSORBED}')
    # Verify applied-in-chunk renames exist (already in the chunk files).
    for sid in RENAMED_IN_CHUNK:
        hits = [it for it in all_items if it['id'] == sid]
        assert len(hits) == 1, f'applied-in-chunk id {sid}: expected exactly 1 item, found {len(hits)}'
    print(f'applied-in-chunk renames present: {RENAMED_IN_CHUNK}')
    # Verify BOTH masala-269 and masala-279 exist as separate items
    # with their exact pages (parent's correction — do NOT treat 279
    # as a duplicate of the renamed 269).
    for sid, exp_pages in BOTH_269_AND_279.items():
        hits = [it for it in all_items if it['id'] == sid]
        assert len(hits) == 1, f'{sid}: expected exactly 1 item, found {len(hits)}'
        assert hits[0]['pages'] == exp_pages, \
            f'{sid}: pages {hits[0]["pages"]} != expected {exp_pages}'
    print(f'both 269 and 279 present as separate items: {BOTH_269_AND_279}')
    ids = [it['id'] for it in all_items]
    assert len(ids) == len(set(ids)), f'STILL DUPLICATE IDS: {[i for i in ids if ids.count(i) > 1]}'
    empty = [it['id'] for it in all_items if not it.get('tashreeh_jawab')]
    assert set(empty) == EMPTY_JAWAB_ALLOWED, \
        f'EMPTY JAWAB mismatch: {sorted(empty)} != {sorted(EMPTY_JAWAB_ALLOWED)}'
    print(f'empty jawab (allow-listed only): {sorted(empty)}')
    empty_sawal = [it['id'] for it in all_items if not it.get('tashreeh_sawal')]
    assert set(empty_sawal) == EMPTY_SAWAL_ALLOWED, \
        f'EMPTY SAWAL mismatch: {sorted(empty_sawal)} != {sorted(EMPTY_SAWAL_ALLOWED)}'
    print(f'empty sawal (by design only): {sorted(empty_sawal)}')
    pages = set()
    for it in all_items:
        pages.update(it['pages'])
    # PRIMARY coverage check (Jild 17 lesson): validate against the 640
    # unique pages directly, not against a range-minus-gaps computation
    # (pp. 167 and 285 are inter-chunk gaps inside NO chunk's span).
    assert len(pages) == 640, f'expected 640 unique pages, got {len(pages)}'
    assert min(pages) == 6 and max(pages) == 720, \
        f'page span {min(pages)}-{max(pages)} != 6-720'
    # Secondary cross-check: per-chunk page union must equal the
    # manifest's unique_pages for that chunk (manifest has no
    # start_page/end_page fields, so no range arithmetic here).
    for entry in manifest['chunks']:
        if entry['chunk'] in merged_chunks:
            # Re-read the chunk file itself: combined items carry pages
            # from several chunks, so per-chunk attribution must come
            # from the raw file, not from the merged items.
            d = json.load(open(os.path.join(base, entry['file']), encoding='utf-8'))
            raw_pages = set()
            for it in d['masail']:
                raw_pages.update(it['pages'])
            assert len(raw_pages) == entry['unique_pages'], \
                f'chunk {entry["chunk"]}: {len(raw_pages)} unique pages != manifest {entry["unique_pages"]}'
            assert len(d['masail']) == entry['items'], \
                f'chunk {entry["chunk"]}: {len(d["masail"])} items != manifest {entry["items"]}'
    print(f'total items: {len(all_items)} | pages covered: {len(pages)}')
    assert len(all_items) == 207, f'expected 207 items after combines, got {len(all_items)}'
    # sort by start_page for the final file
    all_items.sort(key=lambda it: it['start_page'])
    for it in all_items:
        it.pop('_src_file', None)
    if write:
        with open(os.path.join(base, 'jild-24.json'), 'w', encoding='utf-8') as f:
            json.dump({'masail': all_items}, f, ensure_ascii=False, indent=1)
        with open(os.path.join(base, 'chunks-manifest-jild24.json'), 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        print(f'WROTE jild-24.json: {len(all_items)} items, {len(pages)} pages, chunks merged: {merged_chunks}')
    return all_items, pages, merged_chunks


def main():
    manifest_path = os.path.join(BASE, 'chunks-manifest-jild24.json')
    run_merge(manifest_path, BASE, write=True)


if __name__ == '__main__':
    main()
