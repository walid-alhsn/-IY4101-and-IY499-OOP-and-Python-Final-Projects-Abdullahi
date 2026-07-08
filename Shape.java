
import java.util.ArrayList;

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
public abstract class Shape {
    private Coordinates position; // position of the shape
    private int sides; // number of sides of the shape

    // Constructor to initialise the shape with its number of sides and position
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
    public double width; // width of the rectangle
    public double length; // length of the rectangle

    // Constructor to initialize the rectangle with its position, width, and length
    public Rectangle (Coordinates position, double width, double length) {
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
    public double side; // side length of the square

    // Constructor to initialise the square with its position and side length
    public Square (Coordinates position, double side) {
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
    public double radius; // radius of the circle

    // Constructor to initialize the circle with its position and radius
    public Circle(Coordinates position, double radius) {
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
    public Coordinates vertex2; // second vertex of the triangle
    public Coordinates vertex3; // third vertex of the triangle

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

class ShapeList  {
    private ArrayList<Shape> listOfShapes;

    public ShapeList() {
        this.listOfShapes = new ArrayList<Shape>();
    }

    public void addShape(Shape s) {
        listOfShapes.add(s);
    }

    public void translateShapes(int dx, int dy) {
        for (Shape s : listOfShapes) {
            s.translate(dx, dy);
        }
    }

    public Shape getShape(int pos) {
        return listOfShapes.get(pos);
    }

    public Shape removeShape(int pos) {
        return listOfShapes.remove(pos);
    }

    public double area(int pos) {
        return listOfShapes.get(pos).getArea();
    }

    public double perimeter(int pos) {
        return listOfShapes.get(pos).getPerimeter();
    }

    public void scale(int factor, boolean sign) {
        for (Shape s : listOfShapes) {
            s.scale(factor, sign);
        }
    }

    public int getNumberOfShapes() {
        return listOfShapes.size();
    }

    public String display() {
        String d = "";
        for (Shape s : listOfShapes) {
            d += s.display() + "\n";
        }
        return d;
    }

}

class ShapeManagement {
    public static void main(String[] args) {
        ShapeList shapeList = new ShapeList();
        Coordinates c1 = new Coordinates(0, 0);
        Rectangle r1 = new Rectangle(c1, 4, 5, 10);
        shapeList.addShape(r1);
        System.out.println(shapeList.display());
    }
}



