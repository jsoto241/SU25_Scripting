# Jose Soto 
# Text Adventure 
# Game 2341 - Summer  
'''As an agent of chaos(a bored house cat) you are tasked with wandering around this uncivlized environment and enact destruction upon the ignorant inhabitants 
of this confined space as divine retribution for imprisoning such a noble creature such as yourself and as the ultimate act of retaliation you will make sure  
 their precious belongings shall pay the price of their ignorance'''

#Main loop is prompt a surface to navigate to and allows you to choose what you want to knock off and you can obtain 1 of 2 ending normal or lazy cat 



import random
import time

# Delay text output for dramatic effect
def delay_print(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.01)
    print("\n")

# Set of visited surfaces to limit branches
visited = set()
# Items knocked off
knocked_off_items = []
# Tracks if user skipped knocking items
forced_to_choose = False

# Room definitions with their respective surfaces
rooms = {
    "Kitchen": [
        "Kitchen Island", "Pantry Shelf", "Dining Table", "Fridge Top", "Oven Handle",
        "Microwave", "Sink Edge", "Trash Bin Lid", "Window Ledge", "Bar Stool"
    ],
    "Living Room": [
        "Couch", "Coffee Table", "Bookshelf", "TV Stand", "Fireplace Mantle",
        "Armchair", "Side Table", "Rug Center", "Cat Tree", "Curtain Rod"
    ],
    "Bedroom": [
        "Bedroom Dresser", "End Table", "Windowsill", "Desk", "Nightstand",
        "Closet Shelf", "Bed Footboard", "Vanity Table", "Laundry Basket", "Chair Back"
    ]
}

# Each surface mapped to up to three item options
surfaces = {
    "Couch": ["Remote", "Glass of Water"],
    "Coffee Table": ["Succulent", "Picture Frame", "Candle"],
    "Kitchen Island": ["Salt Shaker", "Apple"],
    "Pantry Shelf": ["Jar of Rice", "Can of Soup", "Treat Bag"],
    "Dining Table": ["Vase", "Napkin Holder"],
    "Bookshelf": ["Game Controller", "DVD Case"],
    "End Table": ["Cell Phone", "Pen", "Coffee Pod"],
    "Windowsill": ["Cereal Box", "Plastic Bag"],
    "Bedroom Dresser": ["Alarm Clock", "Book"],
    "Fridge Top": ["Tupperware", "Lemon"],
    "Oven Handle": ["Oven Mitt", "Recipe Card"],
    "Microwave": ["Measuring Cup", "Timer"],
    "Sink Edge": ["Sponge", "Mug"],
    "Trash Bin Lid": ["Empty Can", "Banana Peel"],
    "Window Ledge": ["Succulent", "Measuring Spoon"],
    "Bar Stool": ["Tote Bag", "Notebook"],
    "TV Stand": ["TV Remote", "Speaker"],
    "Fireplace Mantle": ["Clock", "Snow Globe"],
    "Armchair": ["Blanket", "TV Guide"],
    "Side Table": ["Coaster", "Lamp"],
    "Rug Center": ["Cat Toy", "Loose Button"],
    "Cat Tree": ["Feather Toy", "Mouse Toy"],
    "Curtain Rod": ["Clip", "Hair Tie"],
    "Desk": ["Sticky Note", "Pen Cup"],
    "Nightstand": ["Phone Charger", "Earplugs"],
    "Closet Shelf": ["Sweater", "Empty Box"],
    "Bed Footboard": ["Sock", "Rubber Band"],
    "Vanity Table": ["Makeup Brush", "Compact Mirror"],
    "Laundry Basket": ["Shirt", "Underwear"],
    "Chair Back": ["Scarf", "Hat"]
}

# Surface descriptions
surface_descriptions = {
    "Couch": "A plush couch with claw marks. The Remote is barely balanced on one arm.",
    "Coffee Table": "A low wooden table with a Succulent, a Picture Frame, and a Candle.",
    "Kitchen Island": "A sleek granite-topped island. A Salt Shaker and Apple rest close to the edge.",
    "Pantry Shelf": "Tall and full of snacks. A Jar of Rice and a Can of Soup teeter.",
    "Dining Table": "A formal table set for dinner. A Vase and Napkin Holder stand neatly.",
    "Bookshelf": "Tall with many shelves. A Game Controller and a dusty DVD Case tempt fate.",
    "End Table": "Next to a bed. A Cell Phone, a Pen, and a Coffee Pod are on it.",
    "Windowsill": "Sun streams through. A Cereal Box and a Plastic Bag rest there.",
    "Bedroom Dresser": "Drawers closed, mostly. An Alarm Clock ticks and a Book lays halfway open.",
    "Fridge Top": "Dusty and rarely visited. A Tupperware container and a Lemon sit abandoned.",
    "Oven Handle": "Warm to the touch. An Oven Mitt and a dangling Recipe Card sway.",
    "Microwave": "Buzzes faintly. A Measuring Cup and Timer rest on top.",
    "Sink Edge": "Damp and inviting. A Mug teeters beside a Sponge.",
    "Trash Bin Lid": "Smells mysterious. An Empty Can and Banana Peel beg for freedom.",
    "Window Ledge": "Bright and narrow. A Succulent and Measuring Spoon sunbathe.",
    "Bar Stool": "Wobbly and high. A Tote Bag and Notebook barely hold on.",
    "TV Stand": "Glossy and clean. A TV Remote and tiny Speaker sit in wait.",
    "Fireplace Mantle": "Majestic and high. A Clock and Snow Globe beckon.",
    "Armchair": "Comfy and nap-worthy. A Blanket and TV Guide rest gently.",
    "Side Table": "A small table with a Coaster and a Lamp.",
    "Rug Center": "Soft and central. A Cat Toy and Loose Button lie scattered.",
    "Cat Tree": "Tall and owned by you. A Feather Toy and Mouse Toy are temptingly placed.",
    "Curtain Rod": "Precarious and forbidden. A Clip and Hair Tie barely cling.",
    "Desk": "Messy and covered. A Sticky Note and Pen Cup await.",
    "Nightstand": "Bedside and essential. A Phone Charger and Earplugs linger.",
    "Closet Shelf": "Shadowy and quiet. A Sweater and Empty Box lie in rest.",
    "Bed Footboard": "Sturdy and low. A Sock and Rubber Band are balanced there.",
    "Vanity Table": "Pretty and cluttered. A Makeup Brush and Compact Mirror shimmer.",
    "Laundry Basket": "Smelly and full. A Shirt and Underwear are half-hanging out.",
    "Chair Back": "Thin and unsteady. A Scarf and Hat dangle dangerously."
}

# Item fall effects
item_effects = {
    "Remote": "The remote hits the floor with a thud and the batteries roll out.",
    "Glass of Water": "The glass shatters and water spills everywhere!",
    "Succulent": "The pot breaks and dirt scatters.",
    "Picture Frame": "The frame cracks loudly, picture askew.",
    "Candle": "It rolls around, leaving a waxy smear.",
    "Salt Shaker": "Salt sprays like a tiny snowstorm.",
    "Apple": "The apple bounces once, then settles with a bruise.",
    "Jar of Rice": "Glass smashes and rice scatters like sand.",
    "Can of Soup": "It hits with a metallic clunk.",
    "Treat Bag": "It bursts! Treats go everywhere.",
    "Vase": "Water and petals fly as it crashes.",
    "Napkin Holder": "Clinks as napkins flutter.",
    "Game Controller": "Buttons pop loose on impact.",
    "DVD Case": "It skitters, cracking open.",
    "Cell Phone": "Screen cracks spider-web like.",
    "Pen": "Rolls off into oblivion.",
    "Coffee Pod": "It squishes and leaks.",
    "Cereal Box": "Cereal spills in a crunchy avalanche.",
    "Plastic Bag": "It floats down noisily.",
    "Alarm Clock": "Buzzes angrily as it falls.",
    "Book": "Pages flutter dramatically.",
    "Tupperware": "Bounces harmlessly.",
    "Lemon": "Rolls and thuds.",
    "Oven Mitt": "Softly flops to the floor.",
    "Recipe Card": "Drifts like a leaf.",
    "Measuring Cup": "Clinks and spins.",
    "Timer": "Beep echoes as it lands.",
    "Sponge": "Splat!",
    "Mug": "Cracks and spills coffee remnants.",
    "Empty Can": "Rattles loudly.",
    "Banana Peel": "Flops with a squish.",
    "Measuring Spoon": "Tings sharply.",
    "Tote Bag": "Lands with a soft thud.",
    "Notebook": "Flips open mid-air.",
    "TV Remote": "Buttons fly on contact.",
    "Speaker": "Thumps and buzzes.",
    "Clock": "Ticks no more.",
    "Snow Globe": "Shatters in a glittery splash.",
    "Blanket": "Softly lands in a heap.",
    "TV Guide": "Slides under furniture.",
    "Coaster": "Clinks and spins.",
    "Lamp": "Wobbles and dims.",
    "Cat Toy": "Bounces wildly.",
    "Loose Button": "Disappears instantly.",
    "Feather Toy": "Floats down gracefully.",
    "Mouse Toy": "Squeaks as it hits.",
    "Clip": "Snaps apart.",
    "Hair Tie": "Boings once.",
    "Sticky Note": "Drifts like confetti.",
    "Pen Cup": "Pens scatter loudly.",
    "Phone Charger": "Slaps the ground.",
    "Earplugs": "Bounce quietly.",
    "Sweater": "Flops gently.",
    "Empty Box": "Crushes flat.",
    "Sock": "Silently flutters.",
    "Rubber Band": "Snaps in mid-air.",
    "Makeup Brush": "Spins on its bristles.",
    "Compact Mirror": "Cracks down the middle.",
    "Shirt": "Unfolds in flight.",
    "Underwear": "Flies awkwardly.",
    "Scarf": "Curls as it lands.",
    "Hat": "Spins like a frisbee."
}


def get_valid_input(prompt, choices):
    """Prompt user until they pick a valid choice number."""
    while True:
        delay_print(prompt)
        choice = input("> ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(choices):
            return int(choice)
        delay_print(f"Please enter a number between 1 and {len(choices)}.")

def choose_room():
    delay_print("Three rooms lie ahead: Kitchen, Living Room, and Bedroom.")
    rooms_list = list(rooms.keys())
    prompt = "Choose a room to explore:\n"
    for i, room in enumerate(rooms_list, 1):
        prompt += f"{i}. {room}\n"
    choice = get_valid_input(prompt, rooms_list)
    return rooms_list[choice - 1]

def choose_surface(current_room, visited):
    available = [s for s in rooms[current_room] if s not in visited]
    if not available:
        return None  # All visited
    if len(available) == 1:
        # Only one surface left
        return available[0]
    else:
        # Pick 2 surfaces to offer
        choices = random.sample(available, 2)
        prompt = f"Where would you like to go next?\n1. {choices[0]} - {surface_descriptions[choices[0]]}\n2. {choices[1]} - {surface_descriptions[choices[1]]}\n3. Stay at current surface\n"
        choice = get_valid_input(prompt, choices + ["Stay"])
        if choice == 3:
            return None  # Stay at current surface
        else:
            return choices[choice - 1]

def choose_item(surface, forced):
    items_here = surfaces[surface]
    prompt = f"You are at the {surface}.\n{surface_descriptions[surface]}\n"
    for i, item in enumerate(items_here, 1):
        prompt += f"{i}. Knock off the {item}\n"
    prompt += f"{len(items_here)+1}. Leave items alone\n"
    if forced:
        prompt += "You feel compelled to knock something off this time!\n"
    choice = get_valid_input(prompt, items_here + ["Leave alone"])
    return choice

def main():
    delay_print("The cat wakes up, stretches, and surveys its surroundings...\n")
    current_room = choose_room()
    delay_print(f"You are now exploring the {current_room}.\n")
    visited = set()
    knocked_off_items = []
    forced_to_choose = False
    current_surface = None

    while True:
        if current_surface is None:
            next_surface = choose_surface(current_room, visited)
            if next_surface is None:
                # Either no surfaces left or player chose to stay
                if not visited:
                    delay_print("You decide to curl up and take a nap. Nothing was knocked off.\n")
                    break
                else:
                    # End if all surfaces visited or player chooses to quit
                    delay_print("You've explored all surfaces available.\n")
                    break
            else:
                current_surface = next_surface
                delay_print(f"You move to the {current_surface}.\n")
                visited.add(current_surface)
        else:
            # Choose item on current surface
            choice = choose_item(current_surface, forced_to_choose)
            items_here = surfaces[current_surface]
            if choice == len(items_here) + 1:  # Leave items alone
                if forced_to_choose:
                    delay_print("You can't resist the urge anymore! You must knock something off.\n")
                    forced_to_choose = True
                    continue
                else:
                    delay_print("You leave the items alone.\n")
                    forced_to_choose = True
            else:
                item = items_here[choice - 1]
                delay_print(f"You knock off the {item}.\n{item_effects.get(item, '')}\n")
                knocked_off_items.append(item)
                forced_to_choose = False
            # Move from current surface after this choice
            current_surface = None

    # Ending
    if knocked_off_items:
        delay_print("As the mess settles, you revel in your handiwork...\nSuddenly, you hear the door lock turn.\nYour eyes go wide — the owner is home!\n")
    else:
        delay_print("You nap peacefully, leaving everything undisturbed.\n")

if __name__ == "__main__":
    main()

