# coordinator, organizer, branchadmin
#
# object : list[operations]
# 3 types of operations on events: view, create+update+view, full crud 
# 2 types of operations on teams: view, view+delete
# 2 types of operations on participants: view, view+delete
# one operation on coordinators: view+create+delete
# one operation on organizers: view+create+delete
#
# role : list[operations]
# coordinator: view event, view teams, view participants
# organizer: create+update+view event, view+delete teams, view+delete participants, manage coordinators
# branchadmin: all permissive for events releted to their branch, manage organizer
#
# admin can do everything that branchadmin can do but for all events

def role_required() -> None:
    pass