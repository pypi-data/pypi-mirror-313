from stevent_management.db import profiler_collection, event_collection, event_manager_collection
from stevent_management.models import Profiler, EventManager, Event, Ticket
import typer
import csv
from typing_extensions import Annotated






def authenticate(token: str) -> dict:
    decoded_token = EventManager.decode_access_token(token)
    if not decoded_token:
        typer.echo("Invalid or expired token. Please log in again.")
        raise typer.Exit()
    return decoded_token


# Typer CLI app
app = typer.Typer()

@app.command(name="add_event")
def add_event(
    event_name: Annotated[str, typer.Option(prompt=True)],
    description: Annotated[str, typer.Option(prompt=True)],
    event_date: Annotated[str, typer.Option(prompt="Add date as mm-dd-YYYY")],
    age_range: Annotated[str, typer.Option(prompt="Add age range, e.g., 18-25")],  
    token: Annotated[str, typer.Option(prompt=True, hide_input=True)]
):
    # Authenticate the event manager
    authenticated_manager = authenticate(token)
    manager_id = authenticated_manager["sub"]
    typer.echo(f"Authenticated as: {manager_id}")

    # Validate the age_range format (e.g., "18-25")
    try:
        age_min, age_max = map(int, age_range.split('-'))
    except ValueError:
        typer.echo("Invalid age range format. Please use 'min_age-max_age'.")
        raise typer.Exit()

    # Sanitize inputs
    sanitized_eventname = event_name.strip('"')
    sanitized_description = description.strip('"')

    # Create the Event instance
    event = Event(
        event_name=sanitized_eventname,
        description=sanitized_description,
        event_date=event_date,
        age_range=age_range,  # Store the age range as a string, it will be validated later
    )

    # Convert to dictionary and add manager_id
    event_data = event.model_dump()
    event_data["manager_id"] = manager_id  # Add manager_id to associate the event with the manager

    # Insert the event into the database
    event_collection.insert_one(event_data)
    typer.echo(f"Event '{event_name}' created successfully!")


@app.command(name="update_event")
def update_event(
    event_name: Annotated[str, typer.Option(prompt=True)],  # Prompt for event name
    description: Annotated[str, typer.Option()] = None, 
    event_date: Annotated[str, typer.Option()] = None,  
    age_range: Annotated[str, typer.Option()] = None,  
    token: Annotated[str, typer.Option(prompt=True, hide_input=True)] = None,  # Prompt for token
):
    # Authenticate the event manager
    authenticated_manager = authenticate(token)
    manager_id = authenticated_manager["sub"]
    typer.echo(f"Authenticated as: {manager_id}")

    # Sanitize event name
    sanitized_event_name = event_name.strip('"').strip()
    typer.echo(f"Sanitized event name: {sanitized_event_name}")

    # Query for the event
    query = {"event_name": sanitized_event_name, "manager_id": manager_id}
    typer.echo(f"Querying with: {query}")
    event_data = event_collection.find_one(query)

    if not event_data:
        typer.echo(f"No event with the name '{sanitized_event_name}' found for this manager.")
        raise typer.Exit(code=1)

    # Update the event fields
    updated_fields = {}
    if description:
        updated_fields["description"] = description.strip('"').strip()
    if event_date:
        updated_fields["event_date"] = event_date.strip('"').strip()
    if age_range:
        try:
            age_min, age_max = map(int, age_range.split('-'))
            updated_fields["age_range"] = age_range.strip('"').strip()
        except ValueError:
            typer.echo("Invalid age range format. Use 'min_age-max_age'.")
            raise typer.Exit()

    if updated_fields:
        event_collection.update_one(query, {"$set": updated_fields})
        typer.echo(f"Event '{sanitized_event_name}' updated successfully with fields: {updated_fields}")

        # Synchronize updates in profiles collection
        updated_profiles = {}
        if "event_name" in updated_fields:
            updated_profiles["event.event_name"] = updated_fields["event_name"]
        if "event_date" in updated_fields:
            updated_profiles["event.event_date"] = updated_fields["event_date"]
        if "age_range" in updated_fields:
            updated_profiles["event.age_range"] = updated_fields["age_range"]

        if updated_profiles:
            profile_query = {"event.event_name": sanitized_event_name}
            profiler_collection.update_many(profile_query, {"$set": updated_profiles})
            typer.echo(f"Profiles updated to reflect changes in event '{sanitized_event_name}'.")
    else:
        typer.echo("No updates provided. Event remains unchanged.")





@app.command(name="delete_event")
def delete_event(
    event_name: Annotated[str, typer.Option(prompt=True)], 
    token: Annotated[str, typer.Option(prompt=True, hide_input=True)]
):
    # Authenticate the event manager
    authenticated_manager = authenticate(token)
    manager_id = authenticated_manager["sub"]
    typer.echo(f"Authenticated as: {manager_id}")

    # Sanitize event name by stripping quotes and whitespace
    sanitized_event_name = event_name.strip('"').strip()
    typer.echo(f"Sanitized event name: {sanitized_event_name}")

    # Query to find the event for the authenticated manager
    query = {"event_name": sanitized_event_name, "manager_id": manager_id}
    typer.echo(f"Querying with: {query}")

    # Check if the event exists
    event_data = event_collection.find_one(query)
    if not event_data:
        typer.echo(f"No event found with name '{sanitized_event_name}' for this manager.")
        raise typer.Exit(code=1)

    # Delete the event
    event_collection.delete_one(query)
    typer.echo(f"Event '{sanitized_event_name}' deleted successfully!")






def create_profile(username: str, age: int, ticket: str, gender: str, event_name: str, manager_id: str):
    # Sanitize the event name
    sanitized_eventname = event_name.strip('"')
    print(f"Searching for event: '{sanitized_eventname}'")

    # Find the event with the sanitized event_name
    event = event_collection.find_one({"event_name": sanitized_eventname})
    if not event:
        typer.echo(f"Event {sanitized_eventname} not found.")
        raise typer.Exit()

    # Parse the event's age range
    event_obj = Event(**event)

    # Validate the guest's age
    if not (event_obj.age_min <= age <= event_obj.age_max):
        typer.echo(f"Age {age} is not within the allowed range for this event ({event_obj.age_min}-{event_obj.age_max}).")
        raise typer.Exit()

    # Create a Profiler instance
    profile = Profiler(username=username, age=age, ticket=ticket, gender=gender, event=event_obj)
    serialized_profile = profile.model_dump()
    serialized_profile["manager_id"] = manager_id  # Associate the profile with the manager
    print(f"Serialized profile: {serialized_profile}")

    # Insert into the collection
    profiler_collection.insert_one(serialized_profile)
    typer.echo(f"Profile for {username} created successfully!")





@app.command(name="add_profile")
def add_profile(
    username: Annotated[str, typer.Option(prompt=True)], 
    age: Annotated[int, typer.Option(prompt=True)],
    ticket: Annotated[str, typer.Option(prompt=True)],
    gender: Annotated[str, typer.Option(prompt=True)], 
    event_name: Annotated[str, typer.Option(prompt=True)],
    token: Annotated[str, typer.Option(prompt=True, hide_input=True)]
):
    # Authenticate the manager
    authenticated_manager = authenticate(token)
    typer.echo(f"Authenticated as: {authenticated_manager['sub']}")

    # Delegate to create_profile with manager_id
    create_profile(username, age, ticket, gender, event_name, authenticated_manager['sub'])




@app.command(name="list_profiles")
def list_profiles(
    token: Annotated[str, typer.Option(prompt=True, hide_input=True)] = None
):
    # Step 1: Authenticate the manager
    authenticated_manager = authenticate(token)
    manager_id = authenticated_manager['sub']  # Extract the manager's unique ID
    typer.echo(f"Authenticated as: {manager_id}")

    # Step 2: Fetch profiles created by the authenticated manager
    profiles = list(profiler_collection.find({"manager_id": manager_id}, {"_id": 0}))  # Filter by manager_id
    if profiles:
        typer.echo("Profiles in the database:")
        for profile in profiles:
            typer.echo(profile)
    else:
        typer.echo("No profiles found for this manager.")



@app.command(name="get_profile")
def get_profile(
    id: int,
    token: Annotated[str, typer.Option(prompt=True, hide_input=True)] = None
):
    # Authenticate the event manager
    authenticated_manager = authenticate(token)
    manager_id = authenticated_manager["sub"]
    typer.echo(f"Authenticated as: {manager_id}")

    # Query the profile with manager_id
    profile = profiler_collection.find_one({"id": id, "manager_id": manager_id}, {"_id": 0})
    
    if profile:
        typer.echo(profile)
    else:
        typer.echo(f"No profile found with id: {id} for this manager.")




@app.command(name="update_profile")
def update_profile(
    id: Annotated[int, typer.Option(prompt=True)], 
    username: Annotated[str, typer.Option()] = None, 
    ticket: Annotated[str, typer.Option()] = None,
    gender: Annotated[str, typer.Option()] = None,
    age: Annotated[int, typer.Option()] = None,
    token: Annotated[str, typer.Option(prompt=True, hide_input=True)] = None,
):
    # Step 1: Authenticate the manager
    authenticated_manager = authenticate(token)
    manager_id = authenticated_manager["sub"]
    typer.echo(f"Authenticated as: {manager_id}")

    # Step 2: Fetch current profile and validate manager_id
    current_profile = profiler_collection.find_one({"id": id, "manager_id": manager_id}, {"_id": 0})
    if not current_profile:
        typer.echo(f"No profile found with id {id} for this manager. Exiting...")
        raise typer.Exit(code=1)

    # Step 3: Fetch the associated event
    event_data = event_collection.find_one({"event_name": current_profile["event"]["event_name"]})
    if not event_data:
        typer.echo("Event associated with this profile does not exist. Exiting...")
        raise typer.Exit(code=1)
    event_obj = Event(**event_data)

    # Step 4: Prepare updates
    updated_fields = {}
    if username:
        updated_fields["username"] = username

    if ticket:
        if ticket not in Ticket.__members__:  # Validate ticket value
            typer.echo(f"Invalid ticket type: {ticket}. Must be one of {list(Ticket)}.")
            raise typer.Exit(code=1)
        updated_fields["ticket"] = ticket

    if gender:
        updated_fields["gender"] = gender  # Optionally, add validation here

    if age:
        if not (event_obj.age_min <= age <= event_obj.age_max):  # Validate age range
            typer.echo(f"Age {age} is not valid for the event ({event_obj.age_min}-{event_obj.age_max}).")
            raise typer.Exit(code=1)
        updated_fields["age"] = age

    # Step 5: Update in the database
    if updated_fields:
        profiler_collection.update_one({"id": id, "manager_id": manager_id}, {"$set": updated_fields})
        typer.echo(f"Profile with id {id} updated successfully with fields: {updated_fields}")
    else:
        typer.echo("No updates provided. Profile remains unchanged.")



@app.command(name="delete_profile")
def delete_profile(
    id: int,
    token: Annotated[str, typer.Option(prompt=True, hide_input=True)] = None
):
    # Authenticate the event manager
    authenticated_manager = authenticate(token)
    manager_id = authenticated_manager["sub"]
    typer.echo(f"Authenticated as: {manager_id}")

    # Delete the profile with the specified id and manager_id
    result = profiler_collection.delete_one({"id": id, "manager_id": manager_id})
    if result.deleted_count > 0:
        typer.echo(f"Profile with id {id} deleted successfully!")
    else:
        typer.echo(f"No profile found with id: {id} for this manager.")
        raise typer.Exit()


@app.command(name="delete_all_profiles")
def delete_all_profiles(
    token: Annotated[str, typer.Option(prompt=True, hide_input=True)] = None
):
    # Authenticate the event manager
    authenticated_manager = authenticate(token)
    manager_id = authenticated_manager["sub"]
    typer.echo(f"Authenticated as: {manager_id}")

    # Delete all profiles associated with the authenticated manager
    result = profiler_collection.delete_many({"manager_id": manager_id})
    typer.echo(f"All profiles created by manager {manager_id} have been deleted from the database.")


@app.command(name="search_profiles")
def search_profiles(
    id: Annotated[int, typer.Option()] = None,
    username: Annotated[str, typer.Option()] = None,
    age: Annotated[int, typer.Option()] = None,
    ticket: Annotated[str, typer.Option()] = None,
    gender: Annotated[str, typer.Option()] = None,
    token: Annotated[str, typer.Option(prompt=True, hide_input=True)] = None
):
    # Authenticate the manager
    authenticated_manager = authenticate(token)
    manager_id = authenticated_manager["sub"]
    typer.echo(f"Authenticated as: {manager_id}")

    # Build the query
    query = {"manager_id": manager_id}  # Ensure the query is scoped to the authenticated manager
    if id is not None:
        query["id"] = id
    if username:
        query["username"] = username
    if age:
        query["age"] = age
    if ticket:
        query["ticket"] = ticket
    if gender:
        query["gender"] = gender

    # Execute the search query
    profiles = list(profiler_collection.find(query, {"_id": 0}))
    if profiles:
        typer.echo("Matching profiles:")
        for profile in profiles:
            typer.echo(profile)
    else:
        typer.echo("No profiles found matching the criteria.")



@app.command(name="export_profiles")
def export_profiles(
    file_path: Annotated[str, typer.Option(prompt=True)],
    token: Annotated[str, typer.Option(prompt=True, hide_input=True)] = None,
):
    authenticated_manager = authenticate(token)
    typer.echo(f"Authenticated as: {authenticated_manager['sub']}")

    # Retrieve profiles created by the authenticated manager
    profiles = list(profiler_collection.find({"manager_id": authenticated_manager["sub"]}, {"_id": 0}))
    if not profiles:
        typer.echo("No profiles found in the database. Exiting...")
        raise typer.Exit(code=1)

    # Export to CSV
    try:
        with open(file_path, "w", newline="") as file:
            # Create a CSV writer object
            writer = csv.DictWriter(file, fieldnames=profiles[0].keys())
            writer.writeheader()  # Write the header row
            writer.writerows(profiles)  # Write all profiles as rows

        typer.echo(f"Profiles successfully exported to {file_path}!")
    except Exception as e:
        typer.echo(f"An error occurred while exporting profiles: {e}")
        raise typer.Exit(code=1)





@app.command(name="register_manager")
def register_manager(username:Annotated[str, typer.Option(prompt=True)], 
                     password:Annotated[str, typer.Option(prompt=True, confirmation_prompt=True, hide_input=True)] 
                     ):
    """Register a new Event Manager."""
    # Check if the username is already taken
    existing_manager = event_manager_collection.find_one({"username": username})
    if existing_manager:
        typer.echo(f"Username '{username}' is already taken. Please choose another.")
        raise typer.Exit()

    # Hash the password
    hashed_password = EventManager.hash_password(password)
    
    # Insert the new manager into the collection
    manager = {"username": username, "password": hashed_password}
    event_manager_collection.insert_one(manager)

    typer.echo(f"Event Manager '{username}' registered successfully!")



@app.command(name="login_manager")
def login_manager(username:Annotated[str, typer.Option(prompt=True)], 
                     password:Annotated[str, typer.Option(prompt=True, confirmation_prompt=True, hide_input=True)] 

):
    """Authenticate an Event Manager."""
    manager = event_manager_collection.find_one({"username": username})
    if not manager or not EventManager.verify_password(password, manager["password"]):
        typer.echo("Invalid username or password.")
        raise typer.Exit()

    access_token = EventManager.create_access_token(data={"sub": manager["username"]})
    typer.echo(f"Login successful! Your access token is: {access_token}")





@app.command(name="delete_manager")
def delete_manager(username: Annotated[str, typer.Option(prompt=True)]):
    """Delete a specific Event Manager by username."""
    result = event_manager_collection.delete_one({"username": username})
    
    if result.deleted_count > 0:
        typer.echo(f"Event Manager '{username}' deleted successfully!")
    else:
        typer.echo(f"No Event Manager found with username: {username}.")
        raise typer.Exit()


@app.command(name="delete_all_managers")
def delete_all_managers():
    """Delete all Event Managers from the database."""
    result = event_manager_collection.delete_many({})
    
    if result.deleted_count > 0:
        typer.echo(f"All Event Managers have been deleted from the database.")
    else:
        typer.echo("No Event Managers found in the database to delete.")



# Run the Typer CLI app
if __name__ == "__main__":
   app()
