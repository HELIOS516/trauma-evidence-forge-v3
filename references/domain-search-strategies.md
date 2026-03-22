# Domain-Specific PubMed Search Strategies

Structured search templates for each clinical domain. Replace `{CONDITION}` with the specific topic.

## Trauma Surgery

```
Search 1 (Guidelines):     {CONDITION} AND (guidelines OR practice management) AND (EAST OR WEST OR ATLS OR ACS-TQIP)
Search 2 (RCTs):           {CONDITION} AND (randomized controlled trial OR RCT) AND (trauma OR injury)
Search 3 (Meta-analyses):  {CONDITION} AND (meta-analysis OR systematic review) AND (trauma OR injury)
Search 4 (Recent):         {CONDITION} AND (trauma OR injury) AND ("last 5 years"[PDat])
Search 5 (Epidemiology):   {CONDITION} AND (incidence OR prevalence OR epidemiology) AND trauma
Search 6 (Landmark):       {CONDITION} AND (landmark OR seminal OR practice-changing) AND trauma
```

Key societies: EAST, WEST, ATLS, ACS-TQIP, AAST

## Emergency General Surgery

See `references/egs-evidence-guide.md` for full condition-specific strategies.

## Surgical Critical Care

See `references/scc-evidence-guide.md` for full topic-specific strategies.

## Global Surgery

```
Search 1 (Capacity):       {CONDITION} AND (surgical capacity OR surgical access) AND (LMIC OR low-income OR resource-limited)
Search 2 (Outcomes):       {CONDITION} AND (outcomes OR mortality) AND (low-income OR middle-income OR sub-Saharan)
Search 3 (Workforce):      {CONDITION} AND (surgical workforce OR surgeon density OR task-shifting)
Search 4 (Cost):           {CONDITION} AND (cost-effectiveness OR economic evaluation) AND surgery AND LMIC
Search 5 (Policy):         {CONDITION} AND (NSOAP OR national surgical plan OR Lancet Commission) AND surgery
Search 6 (Infrastructure): {CONDITION} AND (infrastructure OR equipment OR facility) AND surgical AND assessment
```

Key literature: Lancet Commission (Meara 2015), GlobalSurg Collaborative, WHO-EESC, COSECSA
