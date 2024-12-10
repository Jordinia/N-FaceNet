import fs from "fs";
import path from "path";
import axios from "axios";
import Client from "ssh2-sftp-client";

// Upload a specific file to the server
async function upToServer(employee_id, localFilePath, fileName) {
    const sftp = new Client();
    const sftpHost = "112.78.144.146";
    const sftpUsername = "jordinia";
    const sftpPassword = "3701";
    const sftpPort = 22098;
    const remoteFolder = `Register/${employee_id}`;

    try {
        await sftp.connect({
            host: sftpHost,
            port: sftpPort,
            username: sftpUsername,
            password: sftpPassword,
        });

        // Check if the folder exists, if not, create it
        const folderExists = await sftp.exists(remoteFolder);
        if (!folderExists) {
            await sftp.mkdir(remoteFolder, true);
        }

        // Upload only the specific file received by the backend
        const remotePath = `${remoteFolder}/${fileName}`;
        await sftp.put(localFilePath, remotePath);
        console.log(`Uploaded ${fileName} to ${remotePath}`);

        await sftp.end();
        return { status: "success", message: "File uploaded successfully." };
    } catch (err) {
        console.error("Error during SFTP upload:", err);
        throw new Error("SFTP upload failed");
    }
}

// Save the image to the employee's folder
async function registerImage(employee_id, base64Data, fileName) {
    const filePath = path.join(process.cwd(), "public", "register", employee_id.toString(), fileName);
    const dir = path.dirname(filePath);

    // Ensure the directory exists
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }

    // Save the image as a file
    fs.writeFileSync(filePath, base64Data, "base64");
    return filePath;
}

// Send the data to the server for registration
// Send the data to the server for registration
async function registerToServer(token, employee_id, filenames) {
    const images = { ...filenames.reduce((acc, filename, i) => ({ ...acc, [`filename_${i + 1}`]: filename }), {}) };

    const data = {
        employee_id: employee_id,
        folder_path: `Register/${employee_id}`, // Set folder_path as the remote SFTP path
        count: filenames.length,
        images: images,
    };

    console.log("Registering images:", data);

    try {
        const endpointUrl = `http://100.71.234.28:5000/employee/face/${token}`;
        const response = await axios.put(endpointUrl, data);

        if (response.status === 200 || response.status === 201) {
            return response.data;
        } else {
            return { error: "Failed to register images on the server." };
        }
    } catch (error) {
        console.error("Error during registration:", error.message);
        return { error: "Error during registration." };
    }
}

export default async function handler(req, res) {
    if (req.method === "POST") {
        const { image, employee_id, token } = req.body;

        if (!image || !employee_id) {
            return res.status(400).json({ error: "Missing image data or employee_id" });
        }

        try {
            const base64Data = image.replace(/^data:image\/png;base64,/, "");
            const timestamp = Date.now();
            const fileName = `${timestamp}.png`;

            // Step 3: Save the image to the employee's folder
            const savedImagePath = await registerImage(employee_id, base64Data, fileName);

            // Step 4: Check if 3 photos are saved, if not, return a message
            const employeeDir = path.join(process.cwd(), "public", "register", employee_id.toString());
            const files = fs.readdirSync(employeeDir);
            const imageFiles = files.filter(file => file.endsWith(".png"));

            if (imageFiles.length >= 3) {
                let i = 0;
                for (const file of imageFiles) {
                    const filePath = path.join(employeeDir, file);
                    const faceUploadResult = await upToServer(employee_id, filePath, file);
                    console.log(`Upload to SFTP result (${++i}): `, faceUploadResult);
                }

                // Step 5: Register images to the server using the token and employee_id
                const registerResult = await registerToServer(token, employee_id, imageFiles);
                if (registerResult.error) {
                    return res.status(500).json(registerResult);
                }

                // Step 6: Once 3 photos are saved, delete them after 3 seconds
                setTimeout(() => {
                    imageFiles.forEach(file => {
                        const filePath = path.join(employeeDir, file);
                        fs.unlinkSync(filePath);
                    });
                    console.log(`All ${imageFiles.length} images deleted for employee ${employee_id}`);
                }, 3000);

                return res.status(200).json({
                    message: "3 photos saved and registered successfully, they will be deleted in 3 seconds!",
                    savedImages: imageFiles.map(file => `/register/${employee_id}/${file}`)
                });
            } else {
                return res.status(200).json({
                    message: `${imageFiles.length} photos saved, waiting for more!`,
                    savedImages: imageFiles.map(file => `/register/${employee_id}/${file}`)
                });
            }
        } catch (error) {
            console.error("Error during operation:", error.message);
            return res.status(500).json({ error: "Failed to process image" });
        }
    } else {
        res.setHeader("Allow", ["POST"]);
        return res.status(405).end(`Method ${req.method} Not Allowed`);
    }
}
