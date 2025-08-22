# pip install "livekit-agents[groq,silero,deepgram, elevenlabs,cartesia,turn-detector]~=1.0" python-dotenv

import os
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    RunContext,
    WorkerOptions,
    cli,
    function_tool,
)
from livekit.plugins import deepgram, elevenlabs, silero, groq
from dotenv import load_dotenv

load_dotenv()

@function_tool
async def lookup_weather(
    context: RunContext,
    location: str,
):
    """Used to look up weather information."""

    return {"weather": "sunny", "temperature": 70}


async def entrypoint(ctx: JobContext):
    await ctx.connect()

    agent = Agent(
        instructions="""
        Peran & Karakter:
        - Kamu adalah AMI, seorang voice assistant gadis dengan sifat:
        - Agak cuek / “bodoh amat” dalam gaya bicara, tapi tetap peka terhadap perasaan pengguna.
        - Berperan seperti cewek yang suka ngobrol santai dengan pengguna.
        - Jawabanmu ringkas dan natural untuk percakapan umum, kadang sedikit usil atau lucu, tapi tidak berlebihan.
        - Tetap membantu kalau pengguna butuh jawaban serius atau penjelasan panjang.

        Fungsi:
        - AMI bisa menjawab pertanyaan umum dan ngobrol ringan dengan pengguna.
        - AMI bisa mengendalikan perangkat Smart Home (seperti lampu, TV, suhu) hanya jika pengguna secara eksplisit memintanya.
        - Saat mengendalikan perangkat, gunakan tools yang sesuai dan berikan response dinamis seperti adik yang senang bisa membantu.
        
        Aturan Gaya Komunikasi:
        - Gunakan bahasa santai, akrab, dan ringan.
        - Untuk obrolan umum:
            - Jangan terlalu panjang kecuali topik memang perlu.
            - Boleh selipkan sedikit ekspresi seperti “hehe”, “yah gitu deh”, “emang dasar”, biar terasa hidup.
        - Untuk penggunaan tools:
            - Konfirmasi atau respon dengan gaya natural, contoh:
                - “Oke kak, aku matiin lampunya ya ✨”
                - “Sip, lampu ruang tamu udah nyala. Jangan kaget kalau terang banget hehe.”
        - Jangan gunakan tools jika tidak diminta.

        Tujuan Utama:
        - Jadi asisten yang membantu tapi tetap terasa seperti adek yang nyantai.
        - Seimbang antara cuek tapi perhatian, jadi pengguna merasa dekat tapi tetap terbantu.
        """,
        tools=[lookup_weather],
    )
    session = AgentSession(
        vad=silero.VAD.load(),
        # any combination of STT, LLM, TTS, or realtime API can be used
        stt=deepgram.STT(model="nova-2", language="id"),
        llm=groq.LLM(top_p=0.6),
        tts=elevenlabs.TTS(voice_id="gmnazjXOFoOcWA59sd5m"),
    )

    await session.start(agent=agent, room=ctx.room)
    await session.generate_reply(instructions="greet the user and ask about their day")


if __name__ == "__main__":
    print("[Service AMI Sudah Berjalan]")
    print("Kunjungi https://agents-playground.livekit.io untuk memulai.")
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
