# what do we want to do 
design a web application for a health insurence company. this application is connected to a database that contains all the company data. so, we need to design the database first then design and build the web application 

after reading the project requirments we made the er diagram. which needed alot of adjustments and itterations to be compatible with our current skill level in designing the web application. and to be itself more logical

## **ER diagram**
##### the first iteration
we have 5 entities: customers. hospitals. claims. plans. dependants. each of them has its attributes based on the project requirments.

we didn't want to add anything additional to the project requirments to reduce the complexity as much as possible cause it's the first time any of us designs a web 
application or learn a backend framwork

*but this design had some issues.*
like what does "plan" here mean? does it mean the 3 plan types that we were told about in the project description? or does it mean the data of each plan that a customer signs or buys to himself or one of his dependants. and how will this be translated in the web application eventually. the problem with this point in design is the hospitals. how would we assign them to a plan type later?

how would we implement the "dependants" ? do we connect it to the customer? but this is a bad design cause this way we let the customer fell data that we don't need. like. if we made him add 6 dependants to his data. those dependants maybe outside or uncovered by his plan. or at least some of them are. 

how would we implement the calims? will we connect it to the customer only or the customer and the plan which the calim will be under. or connect it to the customer, plan, and hospital that the customer was supposed to get the care in. 

##### the second iteration
about the plan-hopital-plan type. we made a seprate entity called plan-type that has the 3 main plan types so we can take thier id and assosiate it to each "plan" that a customer can buy. and to each hospital". there is another solution for this which is to add an attripute to both the plan and hospital and call it "plan-type" without making an entity called plan type. but we implemented the first one

and about the dependants-customers. after some searching we reached a better design. which is to connect the dependants to the plan-data. and not connect them to a cutomer in the first place. this way we will only store the data of the dependants who are covered by a plan that a customer has bought for himself. or covered by a plan that the customer has bought for them. but again. how would we implement this in flask. and how would this affect the design of the application? if we were to add the dependants to each plan. how would we add dependants ? we will need the id of the coresponding plan that we will associate them to. so how will we get the id ? will we make it something consistant from us. so all the dependants that we will add in the future will be added to the same plan ? or we will make it daynamic and the admin can choose the id of the plan he wants to associate the dependant to. implementing this was quite complex for our current level in web programming. so we chose the more easier soultion. which is to connect the dependants to the customer

and about the claims-customer-plan-hospital. it's supposed that each claim to be under a certain plan that the customer has bought to cover it. but implementing this would be complex for us. to make the customer choose which plan does he want to fill this claim under. would require us to get all the plans that the customer has bought previously and to make him choose from them. so we rejected the idea of connecting claims to the plan cause we couldn't implement it. and also about connecting the caims to a hospital. what if he got the health care for a health care provider outside the supported hospitals ? and also if we connected them this way. the user MUST choose a hospital which is covered by the plan that he selected eariler to associate teh claim with. THIS forces us to implement the claims-plan connection first. and then do a similer thing with the hospital. 


*conclusion* :- 
we will have 6 entities
1. customer. that has attriputes *id* and *name*
2. dependats. *weak entity* which is connected to customer with attriputes *name* and *cus-id*
3. claims. which is connected to customer.  with attriputes *cus-id, date, benificary, hospital"health care provider", expensies, description, unresolved
4. plan. which means the "plan-data" we will store the data for each plan that a customer has bought in this entity. with attripute. *type-id, cus-id, benificary*
5. type. which means the "plan-type" this would be a small table with the types of plans that we have. 3. basic, preimum and golden. we will take the id of each plan and associate it with the corresponding plan and hospital
6. hospital. which will be connected to plan-type. attriputes: *name, id, location, type-id*


## **sql script**
this is the part which we will write the sql code that creats the database and the tables. it was quite easy without any complications. we created each table and inserted demo data in them to test that they work well

## **the web app + flask**
we made a minimal front end design that covers the basic project requirments. when we open up the server it takes you directly to the customer page. 

the second iteration on the er diagram came when we tried making the web application. features that we couldn't implement or details that would add more complixity had to be removed to enable us submit a working project even if it didn't look or function the best way, it still works. and that's fine for us due to our current level 

*customer*
a customer can buy a plan or view his plans. or file a new claim

buy plan and file claim are almost the same under the hood. they are both forms that take data from the user and submit it to the server where it takes this data and executes the sql code to add this data to the database. 

view plans is the different one. it fitches the data from the db of all the plans that are bought by this user. making the login is not a requirment. and therefor we made the customer page and all it's inner functions refere to one certain customer. who has a number of plans and can file claims and the claim will have the attripute of his id. cus-id. when, each plan type is a link that the user can click and will send him to a page with all the hospitalls avilable under this plan. we couldn't implement viewing all hospotals covered by lesser plans than the selected one. 


*admin*
admin can add a new hospital, customer, dependant. and they are all forms that submit data to the server that executes sql code to add data to the database

admin can also view all the customers in the database and also view claims and make the unresolved claims a resolved claim

## **Refreneces**
*courses and projects*
[Mysql crash course traversy media](https://youtu.be/9ylj9NR0Lcg)   
[mike dane 4:20 hrs Mysql freecodecamp](https://www.youtube.com/watch?v=HXV3zeQKqGY&t=9055s)    
[clever programmer flask crud app](https://youtu.be/3mwFC4SHY-Y)*  
[Traversy media flask app With authentication and crud](https://youtube.com/playlist?list=PLcDxVjglvA7lwqZ4WfZyBkE0drLI9yf6U)  

*search topics*
[Mysql workbench and server on Ubuntu VM](https://youtu.be/IWXQeXHDerg)  
[mysql with flask](https://youtu.be/hQl2wyJvK5k)  

[HTTP Methods (GET/POST) & Retrieving Form Data](https://www.youtube.com/watch?v=9MHYHgh4jYc)  
[delete all records](https://www.ibm.com/docs/en/db2-for-zos/12?topic=programs-deleting-data-from-tables)  
[insert current date](https://stackoverflow.com/questions/168736/how-do-you-set-a-default-value-for-a-mysql-datetime-column)
[a table with 3 valuse](https://stackoverflow.com/questions/4016145/how-can-i-create-a-table-with-a-column-with-3-only-possible-given-values)  
[weak entity](https://youtu.be/UA4mDnf01qI)  
[representing total participation](https://stackoverflow.com/questions/47557835/representing-total-partial-participation-in-sql-mysql-from-er-diagrams)  
[can a strong entity have total participation](https://stackoverflow.com/questions/47557835/representing-total-partial-participation-in-sql-mysql-from-er-diagrams)  
[strong vs weak entities](https://stackoverflow.com/questions/29690902/strong-vs-weak-entities-mysql)  
