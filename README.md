# Project Contributors

- Mel Harkin
- Dana Le
- Carla Ciar
- Katherine Beringer

# Part 1: Technical Documentation

---

## Context and Objective

In this initial phase, you will focus on creating comprehensive technical documentation that will serve as the foundation for the development of the **HBnB Evolution** application. This documentation will help in understanding the overall architecture, the detailed design of the business logic, and the interactions within the system.

---

## Problem Description

You are tasked with documenting the architecture and design of a simplified version of an AirBnB-like application, named **HBnB Evolution**. The application will allow users to perform the following primary operations:

### User Management
- Users can register, update their profiles, and be identified as either regular users or administrators.

### Place Management
- Users can list properties (places) they own, specifying details such as name, description, price, and location (latitude and longitude).
- Each place can also have a list of amenities.

### Review Management
- Users can leave reviews for places they have visited, including a rating and a comment.

### Amenity Management
- The application will manage amenities that can be associated with places.

---

## Business Rules and Requirements

### **User Entity**
- Each user has a `first name`, `last name`, `email`, and `password`.
- Users can be identified as administrators through a **boolean** attribute.
- Users should be able to:
  - Register
  - Update their profile information
  - Be deleted

### **Place Entity**
- Each place has a `title`, `description`, `price`, `latitude`, and `longitude`.
- Places are associated with the **user who created them** (owner).
- Places can have a **list of amenities**.
- Places can be:
  - Created
  - Updated
  - Deleted
  - Listed

### **Review Entity**
- Each review is associated with a specific **place** and **user**, and includes a `rating` and `comment`.
- Reviews can be:
  - Created
  - Updated
  - Deleted
  - Listed (by place)

### **Amenity Entity**
- Each amenity has a `name` and `description`.
- Amenities can be:
  - Created
  - Updated
  - Deleted
  - Listed

---

### **General Rules**
- Each object should be uniquely identified by an **ID**.
- For audit reasons, the **creation** and **update datetime** should be registered for all entities.

---

## Architecture and Layers

The application follows a **layered architecture** divided into:

### 1. **Presentation Layer**
- Includes the services and API through which users interact with the system.

### 2. **Business Logic Layer**
- Contains the models and the core logic of the application.

### 3. **Persistence Layer**
- Responsible for storing and retrieving data from the database.

---

## Persistence

All data will be **persisted in a database**, which will be specified and implemented in **Part 3** of the project.

---

## Tasks

### ✅ High-Level Package Diagram
- Create a high-level package diagram that illustrates the **three-layer architecture** of the application and the communication between these layers via the **facade pattern**.

### ✅ Detailed Class Diagram for Business Logic Layer
- Design a detailed class diagram for the **Business Logic** layer, focusing on the **User**, **Place**, **Review**, and **Amenity** entities.
- Include their **attributes**, **methods**, and **relationships**.
- Ensure to include the **relationships between Places and Amenities**.

### ✅ Sequence Diagrams for API Calls
- Develop sequence diagrams for at least **four different API calls** to show the interaction between the layers and the flow of information.
- Suggested API calls:
  - User registration
  - Place creation
  - Review submission
  - Fetching a list of places

### ✅ Documentation Compilation
- Compile all diagrams and explanatory notes into a **comprehensive technical document**.

---

## Conditions and Constraints

- The documentation must clearly represent the **interactions** and **flow of data** between the different layers of the application.
- Use **UML notation** for all diagrams to ensure consistency and clarity.
- The **business rules and requirements** outlined above must be accurately reflected in the diagrams.
- Ensure that the diagrams are **detailed enough** to guide the implementation phase in the next parts of the project.

---

## Resources:
### UML Basics

[OOP - Introduction to UML](https://intranet.hbtn.io/concepts/1166)

### Package Diagrams

[UML Package Diagram Overview](https://www.visual-paradigm.com/guide/uml-unified-modeling-language/what-is-package-diagram/)
[UML Package Diagrams Guide](https://www.uml-diagrams.org/package-diagrams.html)

### Class Diagrams

[UML Class Diagram Tutorial](https://creately.com/blog/software-teams/class-diagram-tutorial/)
[How to Draw UML Class Diagrams](https://www.visual-paradigm.com/guide/uml-unified-modeling-language/what-is-class-diagram/)

### Sequence Diagrams

[UML Sequence Diagram Tutorial](https://creately.com/guides/sequence-diagram-tutorial/)
[Understanding Sequence Diagrams](https://www.uml-diagrams.org/sequence-diagrams.html)

### General Diagram Tools

[Mermaid.js Documentation](https://mermaid.js.org/)
[draw.io](https://www.drawio.com/)
[Excalidraw](https://excalidraw.com/)

## Expected Outcome

By the end of this part, you should have a complete set of technical documentation that provides a clear and detailed blueprint for the HBnB Evolution application. This documentation will not only guide you through the implementation phases but also ensure that you have a solid understanding of the application’s design and architecture.

Good luck, and remember to leverage the provided resources and your own research to overcome any challenges you encounter!
