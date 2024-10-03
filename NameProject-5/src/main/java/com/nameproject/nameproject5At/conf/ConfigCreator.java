package com.nameproject.nameproject5At.conf;

import com.nameproject.nameproject5At.NameProjectApplication;
import javafx.application.Platform;
import javafx.scene.control.Alert;
import javafx.scene.control.ButtonType;
import org.yaml.snakeyaml.Yaml;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Map;
import java.util.Optional;

public class ConfigCreator {
    public Map<String, Object> getOrCreateConfigFile() {
        // 检查用户文档是否有配置文件，否则自动创建
        try {
            Path documentsDir = getDocumentsDir();
            Path npDir = documentsDir.resolve("NameProject");
            Path configFile = npDir.resolve("config.yaml");

            // 尝试读取yaml文件
            Map<String, Object> yamlData = readYamlFile(configFile);
            if (yamlData != null) {
                return yamlData;
            }

            Alert alert = new Alert(Alert.AlertType.CONFIRMATION);
            alert.setTitle("请求-文件写入");

            alert.setHeaderText("NameProject5 需要在您的文档文件夹中创建配置文件\nNameProject5 needs to create a configuration file in your Documents folder.");
            alert.setContentText("点击“确定”将写入文件，如果您不同意写入，程序将无法运行\nClick \"OK\" to write the file. If you do not agree to write the file, the program cannot run.");

            Optional<ButtonType> result = alert.showAndWait();
            if (result.get() == ButtonType.OK){

            } else {
                Platform.exit();
                System.exit(0);
            }

            // 文件不存在，创建文件夹
            createFolder(npDir);
            // 创建并写入 YAML 文件
            createYamlFile(configFile);

            // 重新读取并返回yaml文件
            return readYamlFile(configFile);

        } catch (Exception e) {
            System.err.println("Failed to get or create config file.");
            e.printStackTrace();
            return null;
        }
    }

    private static Map<String, Object> readYamlFile(Path filePath) {
        try {
            if (!Files.exists(filePath)) {
                return null; // 文件不存在，返回 null
            }
            String yamlContent = Files.readString(filePath);
            Yaml yaml = new Yaml();
            return yaml.load(yamlContent);

        } catch (IOException e) {
            System.err.println("Failed to read YAML file: " + filePath);
            e.printStackTrace();
            return null;
        }
    }

    private Path getDocumentsDir() {
        // 获取用户主目录
        String userHome = System.getProperty("user.home");
        Path documentsDir;

        if (isWindows()) {
            return Paths.get(userHome, "Documents");
        } else {
            return Paths.get(userHome, "Documents"); // 应该根据实际情况修改这里
        }
    }

    private static boolean isWindows() {
        String os = System.getProperty("os.name").toLowerCase();
        return os.contains("win");
    }

    private static void createFolder(Path folderPath) {
        try {
            Files.createDirectories(folderPath);
            System.out.println("Folder created: " + folderPath);
        } catch (IOException e) {
            System.err.println("Failed to create folder: " + folderPath);
            e.printStackTrace();
        }
    }

    private static void createYamlFile(Path filePath) {
        try (InputStream inputStream = NameProjectApplication.class.getResourceAsStream("config/modelConfigure.yaml")) {
            if (inputStream == null) {
                throw new IOException("Resource not found: /config/modelConfigure.yaml");
            }
            String yamlData = new String(inputStream.readAllBytes());
            Files.writeString(filePath, yamlData);
            System.out.println("YAML file created: " + filePath);
        } catch (IOException e) {
            System.err.println("Failed to create YAML file: " + filePath);
            e.printStackTrace();
        }
    }
}
