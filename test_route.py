import requests
BASE = 'https://x8ki-letl-twmt.n7.xano.io/api:7jKAuXti'
HEAD = {'Authorization': 'Bearer eyJhbGciOiJBMjU2S1ciLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiemlwIjoiREVGIn0.FlUZk8gkRglIVvyfdKARBLdnDwtxC_X7'}
paths = ['/academic_tasks', '/academic_tasks/academic_tasks', '/academic_tasks_GET', '/academic_tasks?debug=true']
for p in paths:
    try:
        r = requests.get(BASE + p, headers=HEAD)
        print(p, r.status_code, r.text[:200])
    except Exception as e:
        print(p, 'ERR', e)
