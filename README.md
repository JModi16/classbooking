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
<img src="static/images/home/classdescription.png">
</details>
<details><summary>Card payment Template</summary>
<img src="static/images/home/cardconfirmation.png">
</details>

## Surface

### **Colour** 
The Colour palette is a mixture of 3 colours. Dark blue for the header, white colour for the main body and Purple for the footer.The buttons consists of red and blue colours.
 

### **Typography** 

Fonts were imported from [Google Fonts](https://fonts.google.com/). 

I selected  "Arial"  as the primary font for the main body and Sans-Serif as the Secondary font . I found the Aerial font is a simple, user-friendly, outstanding and clean typeface that contributes the design. I have used Arial has the primary for my previous 3 projects and wanted to main the font typography.
I selected light blue, white as the main body colors and purple for the footer. 

# Features

## Home Page

## User Functionality

<details><summary>Home Page</summary>
Site is opened on this page
<img src="static/images/home/classhome.png">
</details>
<details><summary>Classes Type</summary>
Students can view a range class types offfered on this platform from the classes page.Clicking on 'Browse Classes' directs you to the same page too.
<img src="static/images/home/classtype.png">
</details>
<details><summary>Instructors</summary>
Students can view a range of Instructors on this page.
<img src="static/images/home/instructors.png">
</details>
<details><summary>Login</summary>
<img src="static/images/home/classlogin.png">
</details> Customer are required to register and login before booking a class
<details><summary>Password Reset</summary>
<img src="static/images/passwordreset.png">
</details> Students can request a password reset should they forget their login details. Entering an email address registered on our system will enable them to receive a password reset link to reset their password.
<details><summary> Instructor profile and Book class</summary> 
<img src="static/image/home/viewbook.png">
</details>Students can view any Instructors profile, view rates and packages information and book a class
<details><summary>Scheduled Class</summary>
<img src="static/images/home/schedule.png">
</details>students can book an upcoming scheduled class with their instructor
<details><summary>Class Packages</summary>
<img src="static/images/home/packages.png">
</details>Students have the option of selecting a package of classes to purchase
<details><summary>Booking Cart</summary>
<img src="static/images/home/cart.png">
</details> Students can view their booking cart displaying class bookings, boooking summary with total cost with the option of proceeding to checkout page, editing a class by removing or going back to classes to view and book a different class type.
<details><summary>Edit Cart</summary>
<img src="static/images/home/editcart.png">
</details> Students can remove a class from the booking cart page
<details><summary>Checkout</summary>
<img src="static/images/home/checkout.png">
</details> At the checkout page, students are presented to enter their card details and complete order. The site is in test mode so only default test card number can be accepted
<details><summary>Confirmation</summary>
<img src="static/images/home/confirmed.png">
</details> Confirmation window that your card details have been accepted
<details><summary>Email Class Booking Confirmation</summary>
<img src="static/images/home/mailconfirm.png">
</details> Confirmation the student has received class booking confirmation
<details><summary>Stripe Transaction Summary</summary>
<img src="static/images/home/stripesuccess.png">
</details> Stripe Dashboard in the Events and Logs show payment has succeeded

 ## Site Admin 
Site Administrators only have priveleges to modify the site such as;  add / remove classes in categories, add, remove or modify class instructors, student profiles, email addresses, add, remove and edit scheduled exercise classes using super user login credentials. Please see below

<details><summary>Admin Site Login</summary>
<img src="static/images/adminlogin.png">
</details> Administrators can login via the site home page using their super user credentials.
<details><summary>Site Administration</summary>
<img src="static/images/classadmin.png">
</details> Administrators can use this section to add / remove classes in categories, add, remove or modify class instructors, student profiles, email addresses, add, remove and edit scheduled exercise classes
<details><summary>Instructors Admin/summary>
<img src="static/images/addremoveinstructors.png">
</details> Administrators can add and remove class Instructors from this Profiles, Instructors
<details><summary>Class Categories</summary>
<img src="static/images/categories.png">
</details> Administrators can add and remove type of classes from Services, Categories
<details><summary>Add a class </summary>
<img src="static/images/addclass.png">
</details>Admins can add / edit or remove a scheduled class
<details><summary>  Classes Scheduled  </summary>
<img src="static/images/scheduledclasses.png">
</details>Admins can view upcoming scheduled classes and past classes in Services, Exercise classes.
<details><summary>  Email   </summary>
<img src="static/images/scheduledclasses.png">
</details>Admins can view upcoming scheduled and past scheduled classes booked by students and past classes in Checkout, Class bookings


### Set Up AWS to store static and media files

1. Sign up to AWS [here](https://aws.amazon.com/).
2. Created an account and logged in, under the All Services>Storage menu, click the link that says S3.
3. On the S3 page create a new bucket. Click the orange button that says 'Create Bucket'
4. Name the bucket and select the closest region to you
5. Under 'Object Ownership' select 'ACLs enabled' and leave the Object Ownership as Bucket owner preferred 
6. Uncheck the 'Block all public access' checkbox and check the warning box to acknowledge that the bucket will be made public, then click create bucket 
7. Once created, click the bucket's name and navigate to the properties tab. Scroll to the bottom and under 'Static website hosting' click 'edit' and change the Static website hosting option to 'enabled'. Copy the default values for the index and error documents and click 'save changes'
8. Now navigate to the permissions tab, scroll down to the Cross-origin resource sharing (CORS) section, click edit and paste in the following code:  

 




