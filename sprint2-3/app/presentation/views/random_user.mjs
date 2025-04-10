import { Router } from "express";


const randomUserRouter = Router();

// random user main route
randomUserRouter.get("/get", (req, res) => {
    res.render("random_user");
});

export default randomUserRouter;
