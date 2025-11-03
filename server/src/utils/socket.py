from src.main import sio

ADMIN_ROOM = "admins"
CLIENT_ROOM = "clients"

# socket io

# ✅ Identify user role & join a room
@sio.event()
async def join_room(sid, data):
    role = data.get("role")
    
    if role == "ADMIN":
        sio.enter_room(sid, ADMIN_ROOM)
        print(f"🛠️ Admin joined room: {sid}")
        await sio.emit("admin_joined", {"message": "Admin Online"}, room=sio)
        
    else:
        sio.enter_room(sid, CLIENT_ROOM)
        print(f"👤 Citizen joined room: {sid}")
        await sio.emit("client_connected", {"message": "Citizen Online"}, room=sio)

# ✅ Citizen reports new incident -> send to admins
@sio.event
async def report_incident(sid, incident_data):
    print(f"🚨 New incident: {incident_data}")

    # Broadcast to admin room only
    await sio.emit("new_incident", incident_data, room=ADMIN_ROOM)

# ✅ Admin dispatches responder -> send to citizen client(s)
@sio.event
async def dispatch_responder(sid, data):
    print(f"🚑 Responder dispatched: {data}")

    # Broadcast to all clients (or you can target by id if tracked)
    await sio.emit("responder_dispatched", data, room=CLIENT_ROOM)

# ✅ Disconnect
@sio.event
async def disconnect(sid):
    print(f"❌ Client disconnected: {sid}")