import { Router } from "express";
import multer from "multer";
import axios from "axios";
import fs from "fs";
import { fileURLToPath } from "url";
import path from "path";
import sharp from "sharp";
import FormData from "form-data";


const __dirname = path.dirname(fileURLToPath(import.meta.url));
const fileIoRouter = Router();

// upload directory
const uploadPath = path.join(__dirname, "../../../uploads");

// configures the storage (creates the directory if it doesn't exist) for multer
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        fs.mkdirSync(uploadPath, { recursive: true });
        cb(null, uploadPath);
    },
    // sets the file name in the uploads directory
    filename: (req, file, cb) => {
        cb(null, file.originalname);
    }
});

const upload = multer({ storage });

const renameFile = async (source, destination) => {
    await fs.promises.rename(source, destination);
};

// function to process images with sharp
const processImage = async (filePath, outputPath, format) => {
    await sharp(filePath)
        .toFormat(format)
        .toFile(outputPath);
};

// define a route to upload the file
fileIoRouter.post("/upload", upload.single("file"), async (req, res) => {
    const file = req.file;

    if (!file) {
        return res.status(400).json({ error: "No file sent" });
    }

    // gets the file extension and defines the paths to the temporary and final files
    const fileExtension = path.extname(file.originalname).toLowerCase().substring(1);
    const tempOutputPath = path.join(uploadPath, `temp-${file.originalname}`);
    const finalOutputPath = path.join(uploadPath, file.originalname);
    
    // file formats
    const imageFormats = ["png", "jpeg", "jpg", "gif", "webp"];
    const videoFormats = ["mp4", "mov", "avi"];
    const textFormats = ["txt", "html", "css", "js", "mjs"];
    const compressedFormats = ["rar", "zip"];
    const voiceFormats = ["mp3"];

    try {
        // processes the file based on its format
        if (imageFormats.includes(fileExtension)) {
            await processImage(file.path, tempOutputPath, fileExtension);
            await renameFile(tempOutputPath, finalOutputPath);
        } else if (
            videoFormats.includes(fileExtension) ||
            textFormats.includes(fileExtension) ||
            compressedFormats.includes(fileExtension) ||
            voiceFormats.includes(fileExtension)
        ) {
            await renameFile(file.path, finalOutputPath);
        } else {
            return res.status(400).json({ error: "File format not supported" });
        }

        // adds file to form for submission to file.io
        const formData = new FormData();
        formData.append("file", fs.createReadStream(finalOutputPath));

        // sends the file to file.io
        const response = await axios.post("https://file.io/?expires=1d", formData, {
            headers: formData.getHeaders(),
        });

        const data = response.data;

        // removes the final file after upload
        fs.unlinkSync(finalOutputPath);

        // returns the file link if the upload is successful
        if (data.link) {
            res.json({ success: true, link: data.link });
        } else {
            res.status(500).json({
                success: false,
                error: "An error occurred when trying to upload files to file.io" 
            });
        }
    } catch (error) {
        console.error("Error:", error);
        res.status(500).json({ success: false, error: "Error uploading the file" });
    }
});

fileIoRouter.get("/", (req, res) => {
    res.render("file_io");
});

export default fileIoRouter;
