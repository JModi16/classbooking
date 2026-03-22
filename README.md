<h1 align="center">Class-Booking</h1>

![Website mock-up](static/images/mockup.png)

Class booking is an e-commerce website project created for a fictional fitness class booking platform based in North West London. The main objective of site is to create a user-fiendly enable students to book a class using an easy and 
intuitive approach. User has four class types to book: Personal training, Yoga, Pilates and Boxercise. The site owner only recommends Instructors who are approved and accredited.

Project was created using Python, Django, HTML5, CSS3, and JavaScript. The data was stored in a PostgreSQL database manipulation and deployed using Heroku. AWS is used for media storage and Stripe to accept payments.
Class-Booking is my forth milestone project for Code Institute's Level 5 Diploma in Web Application Development.

[View the live site](https://class-booking-ed512f961728.herokuapp.com/)

# Table contents
* [Strategy](#strategy)
* [Structure](#structure)
* [Skeleton](#skeleton)
* [Surface](#surface)
* [Features](#features)
    * [Home Page](#home-page)
    * [Product Page](#products-page)
    * [Profile Page](#profile-page)
    * [Contact Form](#contact-form)
    * [Authentication](#authentication)
* [Technologies](#technologies-used)
* [Testing](#testing)
  * [Validation](#validation)
    * [HTML Validation](#html-validation)
    * [CSS Validation](#css-validation)
    * [JavaScript Linting](#javascript-linting)
    * [Python Linting](#python-linting)
    * [Lighthouse Testing](#lighthouse-testing)
    * [Responsiveness](#responsiveness)
* [Manual Testing](#manual-testing)
* [Bugs, Issues and Solutions](#bugs-issues-and-solutions)
* [Future Enhancements](#Future-Enhancements)
* [Deployment](#deployment)
* [Credits](#credits)

## Strategy

### User stories

1. As a first time user, I want to; 

* Search for classes by class type of class from the navigation menu
* Search for a class for unified search input
* Search for classes I am interested in  
* Look for various class instructors, from the Instructors page
* Register my profile as a student
* Login as a student enabling me to create a class booking
* Book  a class according to my schedule and date instructor is available 
* Make a secure payment for a class 
* Receive a class booking confirmation mail

2. A a regular student, I want to;

* Login to view my bookings
* Login to make further class bookings with ease
* Acess the site from various devices with response, clear appearance and functionality
* All the above as the first time user
 
3. As a Site Administrator: I want to 

* Update Class Instructors
* Update class types
* Update photos of class instructors
* Add/Edit/Delete class descriptions
* Add/Edit/Remove class rates and packages
* Access payments received by Stripe using webhooks from my stripe portal
* Update Adhoc site content and data.

* ## Structure

 ### Database Schema
The database was designed using DpDiagram.io. There are 5 tables within this relational database: User, Cake, Customer, Order and OrderItem.
<details><summary>ERD</summary>
<img src="static/images/erdcakes.png">
</details>


## Skeleton
   ### Wireframes

<details><summary>Home Page</summary>
<img src="static/images/home/homepage.png">
</details>
<details><summary>Type of Class</summary>
<img src="static/images/home/typeofclass.png">
</details>
<details><summary>Class Description</summary>
<img src="static/images/classdescription.png">
</details>
<details><summary>Card payment Template</summary>
<img src="static/images/cardconfirmation.png">
</details>

## Surface

### **Colour** 
The Colour palette is a mixture of 3 colours. Dark blue for the header, white colour for the main body and light blue for the footer.The buttons consists of blue colours too.
 

### **Typography** 

Fonts were imported from [Google Fonts](https://fonts.google.com/). 

I selected  "Arial"  as the primary font for the main body and Sans-Serif as the Secondary font . I found the Aerial font is a simple, user-friendly, outstanding and clean typeface that contributes the design. 
I selected light blue, white as the main body colors and purple for the footer.

