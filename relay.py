"""FilePal relay: pairs a sender with a waiting receiver and pipes bytes between them.
Env: RELAY_PORT (default 9000), PING_EVERY seconds (default 25).
The relay only forwards bytes; every transfer still needs the receiver's PIN + approval."""
import asyncio, os

WAIT = {}  # device code -> list of waiting (reader, writer)
PING_EVERY = int(os.environ.get("PING_EVERY", 25))


async def pipe(r, w):
    try:
        while True:
            d = await r.read(262144)
            if not d: break
            w.write(d); await w.drain()
    except Exception:
        pass
    finally:
        try: w.close()
        except Exception: pass


async def handle(r, w):
    try:
        cmd, code = (await asyncio.wait_for(r.readline(), 10)).decode().split()
    except Exception:
        return w.close()
    if cmd == "LISTEN":
        WAIT.setdefault(code, []).append((r, w))
    elif cmd == "CONNECT":
        lst = WAIT.get(code, [])
        while lst:
            lr, lw = lst.pop(0)
            if lw.is_closing(): continue
            lw.write(b"GO\n"); w.write(b"OK\n")
            await asyncio.gather(pipe(r, lw), pipe(lr, w))
            return
        w.write(b"NONE\n"); await w.drain(); w.close()
    else:
        w.close()


async def pinger():
    """Keeps idle listener connections alive through proxies and drops dead ones."""
    while True:
        await asyncio.sleep(PING_EVERY)
        for code, lst in list(WAIT.items()):
            for item in list(lst):
                if item not in lst: continue
                try:
                    item[1].write(b"PING\n"); await asyncio.wait_for(item[1].drain(), 5)
                except Exception:
                    if item in lst: lst.remove(item)
                    item[1].close()
            if not lst: WAIT.pop(code, None)


async def main(port):
    srv = await asyncio.start_server(handle, "0.0.0.0", port)
    asyncio.create_task(pinger())
    print(f"FilePal relay listening on :{port}", flush=True)
    async with srv:
        await srv.serve_forever()

if __name__ == "__main__":
    asyncio.run(main(int(os.environ.get("RELAY_PORT", 9000))))
