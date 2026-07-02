
import java.util.ArrayList;

class Coordinates {
    private int x;
    private int y;

    public Coordinates (int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    public double distance(Coordinates p) {
        double distance = 0;
        return distance;
    }

    public void translate(int dx, int dy) {}

    public void scale(int factor, boolean sign) {}

    public String display() {
        String display = "";
        return display;
    }


}

public abstract class Shape {
    private Coordinates position;
    private int sides;

    public Shape (int sides, Coordinates position) {
        this.sides = sides;
        this.position = position;
    }

    public Coordinates getCoordinates() {
        return position;
    }

    public int getSides () {
        return sides;
    }

    public void setCoordinates (Coordinates newcoord) {}

    public void translate (int dx, int dy) {}

    public void scale (int factor, boolean sign) {}

    public abstract double  getArea();

    public abstract double getPerimeter();

    public abstract String display();

}

class Rectangle extends Shape {
    public double width;
    public double length;

    public Rectangle (Coordinates position, int sides, double width, double length) {
        super(sides, position);
        this.width = width;
        this.length = length;
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



