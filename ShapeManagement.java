import java.util.ArrayList;
import java.util.Scanner;

// Class representing a coordinate point in 2D space
class Coordinates { 
    private int x; // x coordinate
    private int y; // y coordinate

    public Coordinates (int x, int y) {
        this.x = x; 
        this.y = y;
    }
    // Getter methods for x and y coordinates
    public int getX() {
        return x;
    }
    // Getter method for y coordinate
    public int getY() {
        return y;
    }
    // Method to calculate the distance between two coordinates
    public double distance(Coordinates p) {
        int dx = this.x - p.getX();
        int dy = this.y - p.getY();

        return Math.sqrt((dx * dx) + (dy * dy));
    }
    // Method to translate the coordinates by a given amount
    public void translate(int dx, int dy) {
        x = x + dx;
        y = y + dy;
    }
    // Method to scale the coordinates by a given factor
    public void scale(int factor, boolean sign) {
        if (factor == 0) {
            System.out.println("Scale factor cannot be zero.");
            return;
        }

        if (sign) {
            x = x * factor;
            y = y * factor;
        } else {
            x = x / factor;
            y = y / factor;
        }
    }
    // Method to display the coordinates as a string
    public String display() {
        return "X = " + x + ", Y = " + y;
    }


}
// Abstract class representing a shape with a position and number of sides
abstract class Shape {
    private Coordinates position; // position of the shape
    private final int sides; // number of sides of the shape

    // Constructor to initialize the shape with its number of sides and position
    public Shape (int sides, Coordinates position) {
        this.sides = sides;
        this.position = position;
    }
    // Getter method for the position of the shape
    public Coordinates getCoordinates() {
        return position;
    }
    // Getter method for the number of sides of the shape
    public int getSides () { 
        return sides;
    }
    // Setter method to update the position of the shape
    public void setCoordinates (Coordinates newcoord) {
        this.position = newcoord;
    }
    // Setter method to update the number of sides of the shape
    public void translate (int dx, int dy) {
        position.translate(dx, dy);
    }
    // Method to scale the shape by a given factor and sign
    public void scale (int factor, boolean sign) {
        position.scale(factor, sign);
    }

    public abstract double  getArea(); // Abstract method to calculate the area of the shape

    public abstract double getPerimeter(); // Abstract method to calculate the perimeter of the shape

    public abstract String display(); // Abstract method to display the shape's information as a string

}
// Class representing a rectangle shape, extending the Shape class
class Rectangle extends Shape {
    private int width; // width of the rectangle
    private int length; // length of the rectangle

    // Constructor to initialize the rectangle with its position, width, and length
    public Rectangle (Coordinates position, int width, int length) {
        super(4, position);
        this.width = width;
        this.length = length;
    }
    // Overriding the scale method to scale the rectangle's dimensions
    @Override
    public void scale(int factor, boolean sign) {
        super.scale(factor, sign);
        // Check if the scale factor is zero to avoid division by zero
        if (factor == 0) {
            return;
        }

        if (sign) {
            width = width * factor;
            length = length * factor;
        } else {
            width = width / factor;
            length = length / factor;
        }

    }
    // Overriding the getArea method to calculate the area of the rectangle
    @Override
    public double getArea() {
        return width * length; // Formula for area of a rectangle
    }
    // Overriding the getPerimeter method to calculate the perimeter of the rectangle
    @Override
    public double getPerimeter() {
        return 2 * (width + length); // Formula for perimeter of a rectangle
    }
    // Overriding the display method to return a string representation of the rectangle's information
    @Override
    public String display() {
        return "Rectangle: position = (" + getCoordinates().display() + 
        "), width = " + width + 
        ", length = " + length +
        ", area = " + String.format("%.2f", getArea()) + 
        ", perimeter = " + String.format("%.2f", getPerimeter());

    }

}

// Class representing a square shape, extending the Shape class
class Square extends Shape {
    private int side; // side length of the square

    // Constructor to initialize the square with its position and side length
    public Square (Coordinates position, int side) {
        super(4, position);
        this.side = side;
    }
    // Overriding the scale method to scale the square's side length
    @Override
    public void scale(int factor, boolean sign) {
        super.scale(factor, sign);

        // Check if the scale factor is zero to avoid division by zero
        if (factor == 0) {
            return;
        }
        if (sign) {
            side = side * factor;
        } else {
            side = side / factor;
        }
    }
    // Overriding the getArea method to calculate the area of the square
    @Override
    public double getArea() {
        return side * side; // Formula for area of a square
    }
    // Overriding the getPerimeter method to calculate the perimeter of the square
    @Override
    public double getPerimeter() {
        return 4 * side; // Formula for perimeter of a square
    }
    // Overriding the display method to return a string representation of the square's information
    @Override
    public String display() {
        return "Square: position = (" + getCoordinates().display() + 
        "), side = " + side +
        ", area = " + String.format("%.2f", getArea()) + 
        ", perimeter = " + String.format("%.2f", getPerimeter());
    }

}

// Class representing a circle shape, extending the Shape class
class Circle extends Shape {
    private int radius; // radius of the circle

    // Constructor to initialize the circle with its position and radius
    public Circle(Coordinates position, int radius) {
        super(0, position);
        this.radius = radius;
    }
    // Overriding the scale method to scale the circle's radius
    @Override
    public void scale(int factor, boolean sign) {
        super.scale(factor, sign);
        // Check if the scale factor is zero to avoid division by zero
        if (factor == 0) {
            return;
        }
        if (sign) {
            radius = radius * factor;
        } else {
            radius = radius / factor;
        }
    }
    // Overriding the getArea method to calculate the area of the circle
    @Override
    public double getArea() {
        return Math.PI * radius * radius; // Formula for area of a circle
    }
    // Overriding the getPerimeter method to calculate the perimeter (circumference) of the circle
    @Override
    public double getPerimeter() {
        return 2 * Math.PI * radius; // Formula for perimeter (circumference) of a circle
    }
    // Overriding the display method to return a string representation of the circle's information
    @Override
    public String display() {
       return "Circle: center = (" + getCoordinates().display() + 
        "), radius = " + radius +
        ", area = " + String.format("%.2f", getArea()) + 
        ", perimeter = " + String.format("%.2f", getPerimeter());
    }
}

// Class representing a triangle shape, extending the Shape class
class Triangle extends Shape {
    private final Coordinates vertex2; // second vertex of the triangle
    private final Coordinates vertex3; // third vertex of the triangle

    // Constructor to initialize the triangle with its three vertices
    public Triangle (Coordinates vertex1, Coordinates vertex2, Coordinates vertex3) {
        super(3, vertex1);
        this.vertex2 = vertex2;
        this.vertex3 = vertex3;
    }
    // Overriding the translate method to translate all three vertices of the triangle
    @Override
    public void translate(int dx, int dy) {
        super.translate(dx, dy);
        vertex2.translate(dx, dy);
        vertex3.translate(dx, dy);
    }
    // Overriding the scale method to scale all three vertices of the triangle
    @Override
    public void scale(int factor, boolean sign) {
        getCoordinates().scale(factor, sign);
        vertex2.scale(factor, sign);
        vertex3.scale(factor, sign);
    }
    // Overriding the getArea method to calculate the area of the triangle using Heron's formula
    @Override
    public double getArea() {
        double a = getCoordinates().distance(vertex2); // Distance between vertex1 and vertex2
        double b = vertex2.distance(vertex3); // Distance between vertex2 and vertex3
        double c = vertex3.distance(getCoordinates()); // Distance between vertex3 and vertex1
        double s = (a + b + c) / 2; // Semi-perimeter
        return Math.sqrt(s * (s - a) * (s - b) * (s - c)); // Heron's formula
    }
    // Overriding the getPerimeter method to calculate the perimeter of the triangle
    @Override
    public double getPerimeter() {
        double a = getCoordinates().distance(vertex2);
        double b = vertex2.distance(vertex3);
        double c = vertex3.distance(getCoordinates());
        return a + b + c; // Sum of the lengths of the three sides
    }
    // Overriding the display method to return a string representation of the triangle's information
    @Override
    public String display() {
        return "Triangle: vertex1 = (" + getCoordinates().display() + 
        "), vertex2 = (" + vertex2.display() + 
        "), vertex3 = (" + vertex3.display() + 
        "), area = " + String.format("%.2f", getArea()) + 
        ", perimeter = " + String.format("%.2f", getPerimeter());
    }
}

// Class representing a list of shapes, allowing for adding, removing, and manipulating shapes
class ShapeList  {
    private final ArrayList<Shape> listOfShapes; // List to store the shapes

    // Constructor to initialize the ShapeList with an empty list of shapes
    public ShapeList() {
        this.listOfShapes = new ArrayList<>();
    }
    // Method to add a shape to the list
    public void addShape(Shape s) {
        listOfShapes.add(s);
    }
    // Method to translate all shapes in the list by a given amount
    public void translateShapes(int dx, int dy) {
        for (Shape s : listOfShapes) {
            s.translate(dx, dy);
        }
    }
    // Method to get a shape at a specific position in the list
    public Shape getShape(int pos) {
        // Expect 1-based positions: valid when 1 <= pos <= size
        if (pos <= 0 || pos > listOfShapes.size()) {
            System.out.println("Invalid position. No shape exists at position " + pos + ".");
            return null;
        }

        return listOfShapes.get(pos - 1); // Adjusting for 1-based indexing
    }
    // Method to remove a shape at a specific position in the list
    public Shape removeShape(int pos) {
        // Expect 1-based positions: valid when 1 <= pos <= size
        if (pos <= 0 || pos > listOfShapes.size()) {
            System.out.println("Invalid position. No shape exists at position " + pos + ".");
            return null;
        }

        return listOfShapes.remove(pos - 1);
    }
    // Method to calculate the area of a shape at a specific position in the list
    public double area(int pos) {
        Shape shape = getShape(pos);

        if (shape == null) {
            return 0;
        }
        return shape.getArea();
    }
    // Method to calculate the perimeter of a shape at a specific position in the list
    public double perimeter(int pos) {
        Shape shape = getShape(pos);

        if (shape == null) {
            return 0;
        }
        return shape.getPerimeter();
    }
    // Method to scale all shapes in the list by a given factor and sign
    public void scale(int factor, boolean sign) {
        for (Shape s : listOfShapes) {
            s.scale(factor, sign);
        }
    }
    // Method to get the number of shapes in the list
    public int getNumberOfShapes() {
        return listOfShapes.size();
    }
    // Method to display information about all shapes in the list
    public String display() {
        if (listOfShapes.isEmpty()) {
            return "There are no shapes in the list.";
        }

        String d = ""; // An empty string to hold the display information
        // Loop through the list of shapes and append their information to the display string
        for (int i = 0; i < listOfShapes.size(); i++) {
            d += "Shape " + (i + 1) + ": " + listOfShapes.get(i).display() + "\n";
        }
        return d;
    }

     // Translates one shape at a specific position.
    public boolean translateShape(int pos, int dx, int dy) {
        Shape shape = getShape(pos);

        if (shape == null) {
            return false;
        }

        shape.translate(dx, dy);
        return true;
    }

    // Scales one shape at a specific position.
    public boolean scaleShape(int pos, int factor, boolean sign) {
        Shape shape = getShape(pos);

        if (shape == null) {
            return false;
        }

        shape.scale(factor, sign);
        return true;
    }
}

// Main class for managing shapes and user interaction
public class ShapeManagement {
    public static void main(String[] args) {
        try (Scanner input = new Scanner(System.in)) {
            ShapeList shapeList = new ShapeList();
            boolean running = true;
            
            System.out.println("Shape Management Application");
            System.out.println("============================");
            
            while (running) {
                displayMenu();
                int choice = readInt(input, "\nEnter your choice: ");
                
                switch (choice) {
                    case 1 -> addShapeMenu(input, shapeList);
                        
                    case 2 -> removeShapeMenu(input, shapeList);
                        
                    case 3 -> getShapeMenu(input, shapeList);
                        
                    case 4 -> areaAndPerimeterMenu(input, shapeList);
                        
                    case 5 -> {
                        System.out.println("\nAll Shapes");
                        System.out.println("----------");
                        System.out.println(shapeList.display());
                    }
                        
                    case 6 -> translateShapesMenu(input, shapeList);
                        
                    case 7 -> scaleShapesMenu(input, shapeList);
                        
                    case 8 -> translateOneShapeMenu(input, shapeList);
                        
                    case 9 -> scaleOneShapeMenu(input, shapeList);
                        
                    case 10 -> addSampleTestShapes(shapeList);
                        
                    case 11 -> drawGeneralShapeMenu(input);
                        
                    case 0 -> {
                        running = false;
                        System.out.println("Program ended. Goodbye.\n");
                    }
                        
                    default -> System.out.println("Invalid menu choice. Please choose a number from 0 to 11.");
                }
            }
        }
    }

    // Displays the main menu options.
    private static void displayMenu() {
        System.out.println("\nMain Menu");
        System.out.println("---------");
        System.out.println("1. Add a shape");
        System.out.println("2. Remove a shape by position");
        System.out.println("3. Get information about a shape by position");
        System.out.println("4. Display area and perimeter of a shape by position");
        System.out.println("5. Display information of all shapes");
        System.out.println("6. Translate all shapes");
        System.out.println("7. Scale all shapes");
        System.out.println("8. Translate one shape by position");
        System.out.println("9. Scale one shape by position");
        System.out.println("10. Add sample test shapes (Adds shapes required for test plan in brief)");
        System.out.println("11. Draw a general shape");
        System.out.println("0. Quit program");
    }

    // Handles the add shape option.
    private static void addShapeMenu(Scanner input, ShapeList shapeList) {
        System.out.println("\nChoose Shape Type");
        System.out.println("-----------------");
        System.out.println("1. Rectangle");
        System.out.println("2. Square");
        System.out.println("3. Circle");
        System.out.println("4. Triangle");

        int shapeChoice = readInt(input, "\nEnter shape type: ");

        switch (shapeChoice) {
            case 1 -> addRectangle(input, shapeList);

            case 2 -> addSquare(input, shapeList);

            case 3 -> addCircle(input, shapeList);

            case 4 -> addTriangle(input, shapeList);

            default -> System.out.println("Invalid shape type.");
        }
    }

    // Creates and adds a rectangle.
    private static void addRectangle(Scanner input, ShapeList shapeList) {
        System.out.println("\nAdd Rectangle");
        Coordinates position = readCoordinates(input, "position");
        int width = readPositiveInt(input, "Enter width: ");
        int length = readPositiveInt(input, "Enter length: ");

        Rectangle rectangle = new Rectangle(position, width, length);
        shapeList.addShape(rectangle);
        System.out.println("Rectangle added successfully.");
    }

    // Creates and adds a square.
    private static void addSquare(Scanner input, ShapeList shapeList) {
        System.out.println("\nAdd Square");
        Coordinates position = readCoordinates(input, "position");
        int side = readPositiveInt(input, "Enter side: ");

        Square square = new Square(position, side);
        shapeList.addShape(square);
        System.out.println("Square added successfully.");
    }

    // Creates and adds a circle.
    private static void addCircle(Scanner input, ShapeList shapeList) {
        System.out.println("\nAdd Circle");
        Coordinates position = readCoordinates(input, "centre");
        int radius = readPositiveInt(input, "Enter radius: ");

        Circle circle = new Circle(position, radius);
        shapeList.addShape(circle);
        System.out.println("Circle added successfully.");
    }

    // Creates and adds a triangle.
    private static void addTriangle(Scanner input, ShapeList shapeList) {
        System.out.println("\nAdd Triangle");
        Coordinates vertex1 = readCoordinates(input, "vertex 1");
        Coordinates vertex2 = readCoordinates(input, "vertex 2");
        Coordinates vertex3 = readCoordinates(input, "vertex 3");

        Triangle triangle = new Triangle(vertex1, vertex2, vertex3);
        shapeList.addShape(triangle);
        System.out.println("Triangle added successfully.");
    }

    // Handles the remove shape option.
    private static void removeShapeMenu(Scanner input, ShapeList shapeList) {
        int pos = readInt(input, "\nEnter the position of the shape to remove: ");

        Shape existingShape = shapeList.getShape(pos);
        if (existingShape == null) {
            return;
        }

        boolean confirmed = false;

        while (!confirmed) {
            String confirmation = readString(input,
                    "Are you sure you want to remove the shape at position " + pos + "? (yes/no): ")
                    .trim()
                    .toLowerCase();

            if (confirmation.equals("yes") || confirmation.equals("y")) {
                confirmed = true;
            } else if (confirmation.equals("no") || confirmation.equals("n")) {
                System.out.println("Shape removal cancelled.");
                return;
            } else {
                System.out.println("Please enter yes or no.");
            }
        }

        Shape removedShape = shapeList.removeShape(pos);

        if (removedShape != null) {
            System.out.println("\nRemoved shape: " + removedShape.display());
        } else {
            System.out.println("No shape found at the specified position.");
        }
    }

    // Reads a string input from the user.
    private static String readString(Scanner input, String string) {
        System.out.print(string);
        return input.nextLine().trim();
    }

    // Handles the get shape option.
    private static void getShapeMenu(Scanner input, ShapeList shapeList) {
        int pos = readInt(input, "\nEnter the position of the shape: ");
        Shape shape = shapeList.getShape(pos);
        // Check if the shape exists at the given position
        if (shape != null) {
            System.out.println("\nShape information:");
            System.out.println(shape.display());
        } else {
            System.out.println("No shape found at the specified position.");
        }
    }

    // Handles the area and perimeter option.
    private static void areaAndPerimeterMenu(Scanner input, ShapeList shapeList) {
        int pos = readInt(input, "\nEnter the position of the shape: ");
        Shape shape = shapeList.getShape(pos);
        // Check if the shape exists at the given position
        if (shape != null) {
            System.out.println("\nShape name: " + shape.getClass().getSimpleName());
            System.out.println("Area = " + String.format("%.2f", shape.getArea()));
            System.out.println("Perimeter = " + String.format("%.2f", shape.getPerimeter()));
        } else {
            System.out.println("No shape found at the specified position.");
        }
    }

    // Handles the translate all shapes option.
    private static void translateShapesMenu(Scanner input, ShapeList shapeList) {
        int dx = readInt(input, "\nEnter x distance: ");
        int dy = readInt(input, "Enter y distance: ");

        shapeList.translateShapes(dx, dy);
        System.out.println("All shapes translated successfully.");
    }

    // Handles the scale all shapes option.
    private static void scaleShapesMenu(Scanner input, ShapeList shapeList) {
        int factor = readPositiveInt(input, "\nEnter scale factor: ");

        System.out.println("1. Increase/multiply shapes");
        System.out.println("2. Decrease/divide shapes");
        int scaleChoice = readInt(input, "\nEnter scaling option: ");
        // Validate the scaling option input
        while (scaleChoice != 1 && scaleChoice != 2) {
            System.out.println("Invalid option. Choose 1 or 2.");
            scaleChoice = readInt(input, "\nEnter scaling option: ");
        }
        // Determine the sign for scaling based on user choice
        boolean sign = scaleChoice == 1;
        shapeList.scale(factor, sign);
        System.out.println("All shapes scaled successfully.");
    }

    // Reads a pair of x and y coordinates.
    private static Coordinates readCoordinates(Scanner input, String coordinateName) {
        System.out.println("Enter " + coordinateName + " coordinates:");
        int x = readInt(input, "x: ");
        int y = readInt(input, "y: ");
        return new Coordinates(x, y);
    }

    // Reads a whole number safely.
    private static int readInt(Scanner input, String message) {
        System.out.print(message);
        // Loop until a valid integer is entered
        while (!input.hasNextInt()) {
            System.out.println("Invalid input. Please enter a whole number.");
            input.next();
            System.out.print(message);
        }

        int value = input.nextInt();
        input.nextLine();
        return value;
    }

    // Reads a positive whole number safely.
    private static int readPositiveInt(Scanner input, String message) {
        int value = readInt(input, message);
        // Ensure the value is greater than zero
        while (value <= 0) {
            System.out.println("Value must be greater than zero.");
            value = readInt(input, message);
        }

        return value;
    }

    // Handles the translate one shape option.
    private static void translateOneShapeMenu(Scanner input, ShapeList shapeList) {
        int pos = readInt(input, "\nEnter the position of the shape to translate: ");
        int dx = readInt(input, "Enter x distance: ");
        int dy = readInt(input, "Enter y distance: ");

        boolean translated = shapeList.translateShape(pos, dx, dy);
        // Check if the shape was successfully translated and display the result
        if (translated) {
            System.out.println("Shape translated successfully. New position: " + shapeList.getShape(pos).getCoordinates().display());
        } else {
            System.out.println("Shape could not be translated.");
        }
    }

    // Handles the scale one shape option.
    private static void scaleOneShapeMenu(Scanner input, ShapeList shapeList) {
        int pos = readInt(input, "\nEnter the position of the shape to scale: ");
        int factor = readPositiveInt(input, "Enter scale factor: ");

        System.out.println("1. Increase/multiply shape");
        System.out.println("2. Decrease/divide shape");

        int scaleChoice = readInt(input, "\nEnter scaling option: ");
        // Validate the scaling option input
        while (scaleChoice != 1 && scaleChoice != 2) {
            System.out.println("Invalid option. Choose 1 or 2.");
            scaleChoice = readInt(input, "\nEnter scaling option: ");
        }

        boolean sign = scaleChoice == 1;

        boolean scaled = shapeList.scaleShape(pos, factor, sign);

        // Check if the shape was successfully scaled and display the result
        if (scaled) {
            System.out.println("Shape scaled successfully. Updated shape: " + shapeList.getShape(pos).display());
        } else {
            System.out.println("Shape could not be scaled.");
        }
    }

    // Adds the required test shapes from the brief and three extra shapes.
    private static void addSampleTestShapes(ShapeList shapeList) {
        // Required shape 1: triangle
        shapeList.addShape(new Triangle(
                new Coordinates(60, 60),
                new Coordinates(30, 80),
                new Coordinates(80, 80)
        ));

        // Required shape 2: rectangle
        shapeList.addShape(new Rectangle(
                new Coordinates(110, 30),
                20,
                25
        ));

        // Required shape 3: circle
        shapeList.addShape(new Circle(
                new Coordinates(90, 110),
                35
        ));

        // Required shape 4: square
        shapeList.addShape(new Square(
                new Coordinates(100, 50),
                30
        ));

        // Extra shape 1: rectangle of our choice
        shapeList.addShape(new Rectangle(
                new Coordinates(20, 20),
                15,
                10
        ));

        // Extra shape 2: circle of our choice
        shapeList.addShape(new Circle(
                new Coordinates(50, 70),
                12
        ));

        // Extra shape 3: square of our choice
        shapeList.addShape(new Square(
                new Coordinates(75, 40),
                18
        ));

        System.out.println("\nSample test shapes added successfully.");
        System.out.println("Total shapes in list: " + shapeList.getNumberOfShapes());
    }

    // Handles the draw general shape option.
    private static void drawGeneralShapeMenu(Scanner input) {
        System.out.println("\nChoose a shape to draw");
        System.out.println("----------------------");
        System.out.println("1. Rectangle");
        System.out.println("2. Square");
        System.out.println("3. Circle");
        System.out.println("4. Triangle");

        int choice = readInt(input, "\nEnter shape type: ");

        switch (choice) {
            case 1 -> drawRectangle();
            case 2 -> drawSquare();
            case 3 -> drawCircle();
            case 4 -> drawTriangle();
            default -> System.out.println("Invalid shape type.");
        }
    }

    // Draws a general rectangle using text (*) characters.
    private static void drawRectangle() {
        System.out.println("\nGeneral Rectangle");
        System.out.println("-----------------");
        System.out.println("******************");
        System.out.println("*                *");
        System.out.println("*                *");
        System.out.println("*                *");
        System.out.println("******************");
    }

    // Draws a general square using text (*) characters.
    private static void drawSquare() {
        System.out.println("\nGeneral Square");
        System.out.println("--------------");
        System.out.println("*************");
        System.out.println("*           *");
        System.out.println("*           *");
        System.out.println("*           *");
        System.out.println("*           *");
        System.out.println("*           *");
        System.out.println("*************");
    }

    // Draws a general circle using text (*) characters.
    private static void drawCircle() {
        System.out.println("\nGeneral Circle");
        System.out.println("--------------");
        System.out.println("   ******   ");
        System.out.println(" *        * ");
        System.out.println("*          *");
        System.out.println("*          *");
        System.out.println(" *        * ");
        System.out.println("   ******   ");
    }

    // Draws a general triangle using text (*) characters.
    private static void drawTriangle() {
        System.out.println("\nGeneral Triangle");
        System.out.println("----------------");
        System.out.println("     *");
        System.out.println("    ***");
        System.out.println("   *****");
        System.out.println("  *******");
        System.out.println(" *********");
        System.out.println("***********");
    }
}
