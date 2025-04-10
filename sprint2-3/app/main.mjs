import express from "express";
import { engine } from "express-handlebars";
import path from "path";
import { fileURLToPath } from "url";
import { dirname } from "path";
import randomUserRouter from "./presentation/views/random_user.mjs";
import fileIoRouter from "./presentation/views/file_io.mjs";
import previewLinkRouter from "./presentation/views/preview_link.mjs"
import dotenv from "dotenv";


dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// templates and static files dirs 
const templates_dir = path.join(__dirname, "../templates");
const static_dir = path.join(__dirname, "../static");
const handlers_dir = path.join(__dirname, "../app/handlers");

const app = express();
const port = 8000;

// define the template and staticfiles settings
app.set("views", templates_dir);
app.set("view engine", "handlebars");
app.engine("handlebars", engine({ defaultLayout: "base" }));
app.use("/handlers", express.static(handlers_dir));
app.use(express.static(static_dir));

// middleware to process the body of json requests
app.use(express.json());

// rendering the root route
app.get("/", (req, res) => { res.render("home"); });

// set the app to use random user's specific route
app.use("/random-user", randomUserRouter);

// set the app to use file io specific route
app.use("/file-io", fileIoRouter);

// set the app to use preview link specific route
app.use("/preview-link", previewLinkRouter);

app.listen(port, () => {
    console.log(`Listen to port http://localhost:${port}`);
});
