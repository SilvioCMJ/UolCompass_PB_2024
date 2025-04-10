import { Router } from "express";
import axios from "axios";
import dotenv from "dotenv";


dotenv.config();

const previewLinkRouter = Router()

// Get the environment API key
const API_KEY = process.env.PREVIEW_LINK_API_KEY;

// Define a GET route in the root and This route renders the 'preview_link' page
previewLinkRouter.get("/", (req, res) => {
    res.render("preview_link");
});

// Define a POST route in '/api/extract' to extract data from the provided link
previewLinkRouter.post("/api/extract", async (req, res) => {
    const { urlToPreview } = req.body; // Get the URL from the request body

    if (!urlToPreview) {
        return res.status(400).json({ error: "URL is required" });
    }

    try {
        // Make a GET request to the link preview API, using the URL and API key
        const response = await axios.get(
            `https://api.linkpreview.net?key=${API_KEY}&q=${encodeURIComponent(urlToPreview)}`
        );
        res.json(response.data);
    } catch (error) {
        console.error(error);
        res.status(500).send("Request error");
    }
});

// Export the route for use in other modules 
export default previewLinkRouter;
