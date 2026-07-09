# -IY4101-OOP-Java-Project-Abdullahi
This repository contains all code files for my Java Summative 3 Shapes project.
# Shape Management Application

## Project Overview

This project is a Java console-based Shape Management Application developed for the IY4101 Object Oriented Programming assignment. The program allows users to create, store, display, remove, translate, scale, and calculate information about different geometrical shapes.

The application demonstrates key Object-Oriented Programming principles, including encapsulation, abstraction, inheritance, polymorphism, method overriding, and object interaction.

## Main Features

The program provides a menu-driven console interface with the following options:

1. Add a shape
2. Remove a shape by position
3. Get information about a shape by position
4. Display the area and perimeter of a shape by position
5. Display information about all shapes
6. Translate all shapes
7. Scale all shapes
8. Translate one shape by position
9. Scale one shape by position
10. Add sample test shapes
11. Draw a general shape
0. Quit program

The program includes both the required assessment functionality and additional features to improve usability.

## Classes Included

### Coordinates

The `Coordinates` class represents a two-dimensional point using `x` and `y` values.

Main responsibilities:

* Store x and y coordinates
* Return x and y values
* Calculate the distance between two coordinates
* Translate coordinates
* Scale coordinates
* Display coordinate information

### Shape

The `Shape` class is an abstract superclass for all shapes.

Main responsibilities:

* Store the common position of a shape
* Store the number of sides
* Provide shared translate and scale behaviour
* Define abstract methods for area, perimeter and display

The `Shape` class is abstract because a general shape does not have a fixed area or perimeter.

### Rectangle

The `Rectangle` class extends `Shape`.

Attributes:

* `width`
* `length`

Calculations:

* Area = width × length
* Perimeter = 2 × (width + length)

### Square

The `Square` class extends `Shape`.

Attribute:

* `side`

Calculations:

* Area = side × side
* Perimeter = 4 × side

### Circle

The `Circle` class extends `Shape`.

Attribute:

* `radius`

Calculations:

* Area = πr²
* Perimeter = 2πr

### Triangle

The `Triangle` class extends `Shape`.

Attributes:

* Inherited `position` as vertex 1
* `vertex2`
* `vertex3`

The triangle calculates its perimeter by adding the distances between its three vertices. Its area is calculated using Heron’s Formula.

Unlike the other shapes, the `Triangle` class overrides `translate()` and `scale()` so that all three vertices move and scale together.

### ShapeList

The `ShapeList` class manages all shape objects using an `ArrayList<Shape>`.

Main responsibilities:

* Add shapes
* Remove shapes by position
* Get a shape by position
* Calculate area and perimeter by position
* Translate all shapes
* Scale all shapes
* Translate one selected shape
* Scale one selected shape
* Display all shapes

Using `ArrayList<Shape>` allows the program to store rectangles, squares, circles and triangles in one list through polymorphism.

### ShapeManagement

The `ShapeManagement` class contains the main menu and controls user interaction.

Main responsibilities:

* Display the menu
* Read and validate user input
* Create shape objects
* Call methods from `ShapeList`
* Add sample test shapes
* Display general ASCII drawings of shapes

## OOP Principles Demonstrated

### Encapsulation

Class attributes are kept private where possible. For example, shape dimensions such as `width`, `length`, `side`, and `radius` are private. This protects the data and ensures that changes are made through class methods.

### Abstraction

The `Shape` class is abstract. It provides a general structure for all shapes but leaves specific calculations such as area and perimeter to the subclasses.

### Inheritance

`Rectangle`, `Square`, `Circle`, and `Triangle` inherit from `Shape`. This avoids repeated code and allows shared behaviour such as position handling to be placed in one superclass.

### Polymorphism

The `ShapeList` class stores different shape types in one `ArrayList<Shape>`. When methods such as `display()`, `getArea()`, or `getPerimeter()` are called, Java automatically runs the correct version for the actual shape object.

### Method Overriding

Each shape class overrides methods such as `getArea()`, `getPerimeter()`, `scale()`, and `display()` to provide behaviour specific to that shape.

## Sample Test Shapes

The program includes an option to automatically add the required test shapes from the assignment brief, plus three additional shapes.

The sample shapes include:

* Triangle with vertices `(60,60)`, `(30,80)`, and `(80,80)`
* Rectangle at position `(110,30)` with width `20` and length `25`
* Circle at position `(90,110)` with radius `35`
* Square at position `(100,50)` with side `30`
* Extra rectangle
* Extra circle
* Extra square

This feature makes testing faster and more consistent.

## Input Validation

The program validates user input to reduce errors. It checks that:

* Menu choices are valid
* Numeric input is a whole number
* Shape dimensions are greater than zero
* Shape positions exist before getting, removing, translating, or scaling a shape

If the user enters an invalid position, the program displays a clear message instead of crashing.

## Terminal Drawing Feature

The program includes an additional option to draw simple general shapes using text characters.

The available drawings are:

* Rectangle
* Square
* Circle
* Triangle

These drawings are not based on the actual stored dimensions or coordinates. They are included only as a simple visual aid to improve the user experience.

## How to Run the Program

1. Open the project in a Java IDE such as IntelliJ IDEA, Eclipse, NetBeans, or VS Code.
2. Save the file as:

```text
ShapeManagement.java
```

3. Compile the program:

```bash
javac ShapeManagement.java
```

4. Run the program:

```bash
java ShapeManagement
```

5. Use the menu options to add, display, translate, scale, remove, and draw shapes.

## Example Usage

Example flow:

```text
1. Choose option 10 to add sample test shapes.
2. Choose option 5 to display all shapes.
3. Choose option 4 to show the area and perimeter of shape 2.
4. Choose option 6 to translate all shapes.
5. Choose option 7 to scale all shapes.
6. Choose option 11 to draw a general shape.
7. Choose option 0 to quit.
```

## Project Structure

```text
ShapeManagementApplication/
│
├── ShapeManagement.java
├── README.md
└── Report.docx
```
## Assessment Requirements Covered

This project covers the main requirements of the assignment:

- Implements `Coordinates`, `Shape`, `Rectangle`, `Square`, `Circle`, `Triangle`, `ShapeList`, and `ShapeManagement`
- Uses an abstract `Shape` superclass
- Uses inheritance for the four shape subclasses
- Uses polymorphism through `ArrayList<Shape>`
- Calculates area and perimeter for each shape
- Translates and scales shapes
- Handles invalid positions without crashing
- Includes a menu-driven console application
- Includes sample test shapes from the assignment brief
- Includes additional usability features such as individual translate/scale and general shape drawing

## Notes

* The program uses 1-based positions for user interaction.
* Java internally uses 0-based indexing, so the program converts user positions before accessing the list.
* Scaling affects both coordinates and dimensions.
* Integer division is used when scaling down coordinates and dimensions.
* The `Triangle` class scales and translates all three vertices.
* The program avoids crashing when invalid positions are entered.

## Version Control

This project should be stored in a Version Control System such as GitHub or GitLab. Regular commits should show the development progress.

Commit milestones:

1. Initial project setup
2. Add `Coordinates` class
3. Add abstract `Shape` class
4. Add `Rectangle`, `Square`, and `Circle` classes
5. Add `Triangle` class
6. Add `ShapeList` class
7. Add main menu in `ShapeManagement`
8. Add input validation
9. Add individual translate and scale options
10. Add sample test shapes
11. Add general shape drawing option
12. Final testing and report updates

## References

Liang, Y.D. (2021) *Introduction to Java Programming and Data Structures: Comprehensive Version*. 12th edn. Pearson.

Deitel, P. and Deitel, H. (2017) *Java: How to Program, Early Objects*. 11th edn. Pearson.


