# Tools Hub


## Status
`Done`


## Stack
The aplication was developed using `express` with `express-handlebars` for templates management. For the site style was used the `Bootstrap` framework.


## Execution
First clone this repository using:  
``` shell
git clone https://github.com/Compass-pb-aws-2024-JUNHO/sprints-2-3-pb-aws-junho.git

```
Or (if you have ssh configured)  
``` shell
git clone git@github.com:Compass-pb-aws-2024-JUNHO/sprints-2-3-pb-aws-junho.git 

```

Change to branch grupo-3 using: `git switch grupo-3`

Run it in the terminal to install the dependencies:
``` shell
npm install
```


Create a `.env` file and insert the credentials of `local.env`


### Application
To start the aplication:
```bash
npm run start
```
and access: http://localhost:8000


## Application Display
![Application Home Page](/static/img/application-display.png)

Visit the platform through the provided link: http://54.196.252.93:8000/

#### For more informations about the project, see [Design Docs](docs/Design%20Docs%20-%20Tools%20Hub.md)


## Development
### Details
To organize development and maintain good project progress, a board was created on [Trello](https://trello.com/) with the necessary stages to be followed.

When a problem arose that could compromise the progress of tasks delegated to each team member, the procedure was to allocate additional team  
members and instruct them to assist with the solution of the problem in a more **efficient** manner.


### Difficulties
The [Kinde](https://kinde.com/) API was initially implemented to authenticate users and allow access to other resources.  
During the deployment phase, we encountered the issue:  
- The callback URLs in the production environment should have the HTTPS security protocol, but this was not mentioned in the API documentation.  
- Therefore, to ensure the project was delivered on time, we decided to remove this service from the application scope.
