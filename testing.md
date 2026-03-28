# Class-Booking - Testing

![Responsive Mockup](documentation/readme/images/mockup.png)


## Contents
* [Manual Testing](#testing)
  * [Testing User Stories](#testing-user-stories)
  * [Testing Site Functionality](#testing-site-functionality)
  * [Further Testing](#further-testing)
* [Automated testing](#automated-testing)
  * [HTML validation](#html-validation)
  * [CSS validation](#css-validation)
  * [Javascript validation](#javascript-validation)
  * [Python validation](#python-validation)
  * [WAVE Testing](#wave-testing)
  * [Lighthouse](#lighthouse)
* [Bugs](#bugs)
  * [Fixed Bugs](#fixed-bugs)
 
 -   ### Testing User Stories

    -   #### Viewing and Navigation

        1. As a site user, i want to be able to view the website on a range of device sizes and it needs to be aesthetic and functional
        - Site is responsive on devices from 280px
        - Navbar available on each page for ease of navigation
        2. As a parent/guardian, i want to easily understand the purpose of the website
        - The navbar and hero image on the index page instantly informs the user of the site name in the logo and what the business does in the text on the hero image.
        - The colourful design and choice of images supports the message of what the business does.

        - The navbar has a dropdown menu names 'Instructors' , Classeseasily visible on each page.
        - Clicking the courses dropdown shows the user lots of options for information on our different courses and also able to view all courses available
        - There are pages specific to each of the four age categories which gives more in depth information to the user alongside the age-specific course availability so that users can add the course straight to their bag.

        4. As a parent/guardian, i want to be able to see the available courses, the course dates and times so that i can decide if it is suitable to book.
        - Each age-specific group has its own webpage with specific information related to the course, this includes all course-specific availability so the user can easily book once they have found which course is best for their child.
        - From the all courses page the user is able to see all courses, dates and times available and can click on any date which will take them to the course details page for more information and booking options.

        5. As a registered site user, i want to view the contents of my booking cart and be able to add, edit or delete classes
        - The shopping bag is shown as a Bag icon and price located in the top left corner of each webpage. It is in the same location regardless of where the user is within the site or what device they are viewing the site on. 
        - The price is displayed below the Bag icon and is updated with any changes to the shopping bag contents so the user can quickly and easily see their bag total.
        - Clicking on the shopping bag  takes the user to the Shopping Bag page where they are shown the contents of their bag with the relevant course details so they can clearly see what they are wanting to order.
        - The bag contents can easily be updated or removed using the +/- and update/remove buttons on each order item.
        - If the shopping bag is empty, the user is shown a message to inform them of this and directed to the course details buttons for each age group.

        6. As a registered site user, i want to have a personlalised profile where i am able to view my order history and update my profile details
        - Each registered user has a profile which can be found in the Accounts dropdown in the top left corner of the webpage
        - On clicking 'My Profile' within the Account dropdown, the user is taken to their profile page. 
        - The profile page is split into two areas. The first area shown the user their saved Billing Info(if they have chosen to save it at a previous checkout) and they can update their information directly from this page. The next section is an order summary, showing a list of all previous orders.

        7. As a parent/guardian, i want to be abe to meet the team who run the courses and understand more about them and their qualifications so that i know the sessions are being run by competent practitioners
        - Within the navbar 'About' dropdown, a 'Meet the team' link takes the user to the associated are on the home page. Here, the user can find some information about the team with links to view more details about each team member. 
        - On clicking the links, the user is taken to the Meet The Team page. An image of each team member is displayed and hen the user hovers over the picture, the team members name and course speciality is shown alongside a button linking to their own page.
        - If the user then clicks the button on the instructor image, they are taken to that instructors' details page which shows some information named 'a bit about me'. This gives the user a friendly summary of the instructors' relevant qualifications and past work history.

        8. As a parent/guardian, i want to be able to see where the courses are being held so that i know where i am going to be traveling to and can plan my journey

        9. As a site user, i want to be able to contact the site owners if i have any queries and receive email confirmation that my message has been successfully sent
        - From the navbar the user can view the 'Contact' link. When clicked, this takes the user to the Booking Enquiry page where they can fill in a short form and submit. 
        - They will get an email to say that Little Pont have received their enquiry and will get back to them shortly.

        10. As a parent/guardian, i want to be able to make a party booking enquiry
        - From the navbar the user can view the 'Contact' link. When clicked, this takes the user to the Booking Enquiry page where they can fill in a short form and submit. 
        - They will get an email to say that Little Pont have received their enquiry and will get back to them shortly.
        
    
    -   #### Registration and User Account

        1. As site user, i want to be able to easily register as a student.
        2. As a registered user, i want to easily be able to login and logout of my account
        3. As a registered user, i want to be able to reset my password if i have forgotten it
        5. As registered user, i want to ensure all form fields are completed correctly
        
    

    -   #### Purchasing and Checkout
        1. As a logged in user i want to select and book  a class for myself
        2. As a site user, i want an easy and streamlined payment process
        3. As a site administrator, i want to be able to track all details of my class booking, ensuring that I have received a booking confirmation mail with relevant information and  of details my booking are visible on my booking profile

    -   #### Site Administrator
    
        1. As a site admin, i want to easily be able to add, edit or delete classes, Instructors, Instructor profile, registered users profiles a users order in case they have made a booking error and it needs to be amended, in order to provide a good user experience for them.
        2. As a site admin I want to be able to create classes according to the Instructors schedule and availability
        


