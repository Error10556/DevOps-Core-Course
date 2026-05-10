/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `npm run dev` in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run `npm run deploy` to publish your worker
 *
 * Bind resources to your worker in `wrangler.jsonc`. After adding bindings, a type definition for the
 * `Env` object can be regenerated with `npm run cf-typegen`.
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */

async function get_counter(env: Env): Promise<number> {
	const count = await env.KV.get("counter");
	if (count === null) {
		return 0;
	}
	return Number.parseInt(count);
}

async function inc_counter(env: Env): Promise<void> {
	const count = await get_counter(env);
	await env.KV.put("counter", (count + 1).toString());
}

export default {
	async fetch(request: Request, env: Env): Promise<Response> {
		const url = new URL(request.url);
		console.log("path", url.pathname, "colo", request.cf?.colo);

		if (url.pathname === "/health") {
			return Response.json({ status: "ok" });
		}

		if (url.pathname === "/") {
			await inc_counter(env);
			return Response.json({
				app: env.APP_NAME,
				message: "Hello from Cloudflare Workers",
				timestamp: new Date().toISOString(),
			});
		}

		if (url.pathname === "/counter") {
			return Response.json({
				count: await get_counter(env)
			});
		}

		if (url.pathname === "/edge") {
			return Response.json({
				colo: request.cf?.colo,
				country: request.cf?.country,
				city: request.cf?.city,
				asn: request.cf?.asn,
				httpProtocol: request.cf?.httpProtocol,
				tlsVersion: request.cf?.tlsVersion,
			});
		}


		return new Response("Not Found", { status: 404 });
	},
};
