# Animathica

Animated math calculator based on Alan Becker's [Animation Vs Math](https://www.youtube.com/watch?v=B1J6Ou4q8vE&ab_channel=AlanBecker)

See the [discord](https://discord.gg/CQnvNZPefv) for updates.

Working alongside [Quantodeluz](https://github.com/Quantodeluz).

---
Everything past this point is mostly tentative.

## Gameplay

The general idea is to have a canvas onto which you can put symbols you've collected. You can combine symbols to make new symbols, or to create expressions which the system can calculate and thus create new symbols.

### Super Tentative Gameplay Mechanics

- **Library:** Save elements for later use.

1. **Symbol Manipulation:**
   - **Dragging and Dropping:** Move elements on the canvas.
   - **Shift+Drag:** Duplicate an element.
   - **Space:** Evaluate selected expression.
   - **Double-Click:** Separate symbol into sub-symbols?
   - **Click and Drag:** Create a selection square.
   - **Control+Click:** Rotate the selected region.
   - **Alt+Click:** Resize selected region.
   - **Right-Click:** Open options menu.

Tentative.
   - **Contextual Meaning:** Ability to change the meaning or context of different symbols based on their usage in different parts of math.
   - **Defining New Symbols:** Players can define new symbols logically and add them to the library.

### Modes and Levels
1. **Tutorial:**
   - Start with just a '1'.
   - Introduce different types of objects (Symbols, Graphing, Characters, etc.).
   - Culminate in escaping to the imaginary plane using 'i' to create a portal.

2. **Main Menu:**
   - Access after completing tutorial.
   - Modes: Free Mode, Limited Mode, and Level Select.
   - **Free Mode:** Store all symbols unlocked.
   - **Limited Mode:** Start with just '1' and a graphing dot.

### UI and Interaction
1. **Rendering System:**
   - Display individual characters on a canvas using a monospaced font.
   - Store position and rotation of characters.
   - Handle rendering of equations and expressions.

3. **Scope Detection:**
   - Function called `gather_lines` to determine if symbols are part of the same expression (e.g., `1+1` recognized as `1+1`).
   - Handle joining of symbols (e.g., `1`, `+`, and `1` to form `1+1`).

### Back-End System
1. **Gathering and Calculating:**
   - Function to detect scopes and re-run detection when a symbol is selected and space is pressed.
   - Calculation step spawns or removes objects based on the gathered data.
   - Contextual interpretation of symbols based on their mathematical context.

2. **Mathematics Handling:**
   - Underlying calculator to handle mathematical operations and calculations.
   - Support for defining and using new symbols.

## Folder Structure
```
Animathica
|- __main__.py   # Handles system arguments (sys.vargs)
|- Main/         # Folder where main menu and related components are kept (Flow of the game)
|- Canvas/       # Folder where all the graphics and controls on the blackboard are handled by the front-end (Math space)
|- Levels/       # Folder where levels are stored
|- Gather/       # Folder where tables are stored and the gathering logic is implemented
|- Calculator/   # Folder where abstract math calculations occur
|- Symbols/      # Folder for defining and managing symbols and their contexts
```

