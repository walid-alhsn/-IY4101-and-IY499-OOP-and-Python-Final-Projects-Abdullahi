
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
        return "Rectangle: position = (" + getCoordinates().getX() + ", " + getCoordinates().getY() + 
        "), width = " + width + 
        ", length = " + length +
        ", area = " + String.format("%.2f", getArea()) + 
        ", perimeter = " + String.format("%.2f", getPerimeter());

    }

}

class Square extends Shape {
    public double side;

    public Square (Coordinates position, int sides, double side) {
        super(sides, position);
        this.side = side;
    }

    @Override
    public double getArea() {
        double a = 0;
        return a;
    }

    @Override
    public double getPerimeter() {
        double p = 0;
        return p;
    }

    @Override
    public String display() {
        String d = "";
        return d;
    }
    

}

class Circle extends Shape {
    public double radius;

    public Circle(Coordinates position, int sides, double radius) {
        super(sides, position);
        this.radius = radius;
    }

    @Override
    public double getArea() {
        double a = 0;
        return a;
    }

    @Override
    public double getPerimeter() {
        double p = 0;
        return p;
    }

    @Override
    public String display() {
        String d = "";
        return d;
    }


}

class Triangle extends Shape {
    public Coordinates vertex2;
    public Coordinates vertex3;

    public Triangle (int sides, Coordinates vertex1, Coordinates vertex2, Coordinates vertex3) {
        super(sides, vertex1);
        this.vertex2 = vertex2;
        this.vertex3 = vertex3;
    }

    @Override
    public double getArea() {
        double a = 0;
        return a;
    }

    @Override
    public double getPerimeter() {
        double p = 0;
        return p;
    }

    @Override
    public String display() {
        String d = "";
        return d;
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



