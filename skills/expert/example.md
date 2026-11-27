# expert: full example

Input:

```text
I want to add a cache to my web app's product search endpoint because it feels slow. /expert
```

Output (the rewritten prompt):

````
I want to make product search feel fast to the people using it. You've told me it "feels slow" and that a cache is the fix. Before I add a cache, I want to find out where the time goes. Then I want a cache only if the evidence says one helps, and I want it to be one that never serves wrong results. Please do this the way a performance engineer would, not by adding a cache at the first layer you see.

Field: web backend performance engineering.

1. Done when: on a recorded sample of real search queries, p50 and p95 latency of the endpoint are measured before and after the change. The p95 drop is reported with the hit rate. A test shows that a product edit (price, stock, delisting) is never hidden behind a stale cached result longer than the staleness I accept.

2. Expert moves:
   - Treat "feels slow" as a hypothesis. I'm taking that from you as stated (not checked: said by the user). Measure first. The slowness may come from the database query, a missing index, the payload size, an N+1 pattern, or the frontend, and a cache would hide all of those rather than fix them.
   - Look at the query distribution before choosing a design. Search traffic is usually a long tail, so many queries are unique and a cache gets a low hit rate. I don't know the base rate for this app (not checked: no logs available). Take the hit rate from the real query logs, not from an assumption.
   - Decide the staleness budget and the invalidation rule before writing code. Ask me how stale a price or stock count may be. Don't pick a TTL yourself.

3. Raw material: the endpoint's handler and the query it runs (not checked: I haven't seen them, and I don't know the language, framework or datastore). The production or staging access logs with real query strings and timings. The database's query plan for the slow queries (`EXPLAIN ANALYZE` if it's Postgres, which is not checked). Any APM or tracing data that already exists. I don't know where these live in your setup, so ask me.

4. Methods:
   - Start with the USE/RED approach (Brendan Gregg's USE method and Tom Wilkie's RED method). Check Rate, Errors and Duration for the endpoint, then trace one slow request through each stage (handler, query, serialization, network) to find the bottleneck. Only a bottleneck that repeats identical work justifies a cache.
   - If a cache is justified, follow the cache-aside pattern, so the database stays the source of truth. Key it on normalized query parameters (lowercased and trimmed query, filters, sort, page). Add single-flight or request coalescing to prevent a stampede when a hot entry expires. Choose the invalidation strategy (short TTL, event-based invalidation on product writes, or both) from the staleness budget in step 2.
   - Measure with a load tool such as `k6`, `wrk` or `hey`, replaying the sampled real queries and not one repeated query. Report percentiles, not averages. I haven't checked which of these is installed here.

5. External check:
   - You can run this yourself: replay the same query sample against the endpoint before and after. Pass means p95 improves by a margin we agree on in advance and the cached responses are byte-identical to uncached ones for the same query. Fail means either condition doesn't hold.
   - Also run an automated staleness test. Update a product, then search for it. Pass means the new data shows up within the staleness budget.
   - Beyond those, a real-user signal such as production p95 or a slow-search complaint rate after rollout confirms the result.

6. Likely failure: the cache goes in, the hit rate is low (say under 20%) because queries are mostly unique, and p95 barely moves. Meanwhile stale prices or stock counts reach customers. The early signal is the hit rate and the share of unique queries in the log sample. If most queries are unique, stop and fix the query, the index or the payload instead.

7. Off the table:
   - Don't change search relevance or ranking, because the cache must not alter results.
   - Don't change the database schema or add infrastructure (Redis, a CDN) without asking me, because that is a larger commitment than I've agreed to. An in-process cache is fine to try first.
   - Don't touch other endpoints. I only asked about product search.
   - Don't cache user-specific or permission-dependent results under a shared key, so one customer never sees another's data.

8. Not checked: everything about my app. I haven't verified the stack, the datastore, the traffic volume, or whether the endpoint is actually the slow part. I'm taking that from you as stated (not checked: said by the user). One finding would overturn the premise: if the time is spent outside the endpoint (the frontend, network or rendering), or in a query that an index would fix, then a cache is the wrong tool.

9. First step: find the code and logs. Ask me where the endpoint lives and how I can get a sample of real search queries with timings. Then time one slow request stage by stage, before touching any caching code.
````

Produced by Claude Sonnet with this skill, in an empty folder with no access to the app.
