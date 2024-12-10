import fs from "fs";
import path from "path";
import axios from "axios";
import Client from "ssh2-sftp-client";

// Upload a specific file to the server
async function upToServer(employeeId, localFilePath, fileName) {
    const sftp = new Client();
    const sftpHost = "112.78.144.146";
    const sftpUsername = "jordinia";
    const sftpPassword = "3701";
    const sftpPort = 22098;
    const remoteFolder = `Checkin/${employeeId}`;

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

export default async function handler(req, res) {
    if (req.method === "POST") {
        const { image, prefix, employee_nik } = req.body;

        if (!image || !prefix || !employee_nik) {
            return res.status(400).json({ error: "Missing image data, prefix, or employee NIK" });
        }

        try {
            // Step 1: Fetch employee_id using employee_nik
            const employeeResponse = await axios.get(`http://localhost:5000/employee?nik=${employee_nik}`);
            const employeeData = employeeResponse.data.data;
            const employee_id = employeeData[0]?.employee_id;

            if (!employee_id) {
                return res.status(404).json({ error: "Employee not found" });
            }

            // Step 2: Decode base64 image and construct the filename
            const base64Data = image.replace(/^data:image\/png;base64,/, "");
            const timestamp = Date.now();
            const fileName = `${prefix}-${timestamp}.png`;
            const filePath = path.join(process.cwd(), "public", "checkin", employee_id.toString(), fileName);

            // Step 3: Ensure the "employee_id" directory exists and save the image
            const dir = path.dirname(filePath);
            if (!fs.existsSync(dir)) {
                fs.mkdirSync(dir, { recursive: true });
            }
            fs.writeFileSync(filePath, base64Data, "base64");

            // Step 4: Check if both the face and body images exist in the directory
            const employeeDir = path.join(process.cwd(), "public", "checkin", employee_id.toString());
            const files = fs.readdirSync(employeeDir);

            // Filter for images with the prefix 'F' (face) and 'B' (body)
            const faceImage = files.find(file => file.startsWith('F-'));
            const bodyImage = files.find(file => file.startsWith('B-'));

            // If both images exist, proceed with the POST request
            if (faceImage && bodyImage) {
                const images = {
                    captured_face: faceImage,
                    captured_body: bodyImage,
                };

                // Upload both images to the server
                const faceFilePath = path.join(employeeDir, faceImage);
                const bodyFilePath = path.join(employeeDir, bodyImage);

                const faceUploadResult = await upToServer(employee_id, faceFilePath, faceImage);
                const bodyUploadResult = await upToServer(employee_id, bodyFilePath, bodyImage);

                console.log("Upload to SFTP result (face):", faceUploadResult);
                console.log("Upload to SFTP result (body):", bodyUploadResult);

                // Step 5: Make the POST request to your backend
                const checkinResponse = await axios.post(`http://localhost:5000/entry/checkin/${employee_id}`, {
                    images,
                    path: `/checkin/${employee_id}/${faceImage}`,
                });

                // Log the response from the checkin POST request
                console.log("Check-in response:", checkinResponse.data);

                // Step 6: Delete the images after the post request
                fs.unlinkSync(faceFilePath);
                fs.unlinkSync(bodyFilePath);

                return res.status(200).json({
                    message: "Images saved, uploaded, and processed successfully!",
                    paths: [
                        `/checkin/${employee_id}/${faceImage}`,
                        `/checkin/${employee_id}/${bodyImage}`,
                    ],
                });
            }

        } catch (error) {
            console.error("Error during operation:", error.message);
            return res.status(500).json({ error: "Failed to save and upload image" });
        }
    } else {
        res.setHeader("Allow", ["POST"]);
        return res.status(405).end(`Method ${req.method} Not Allowed`);
    }
}