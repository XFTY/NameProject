/* Copyright 2024-2025 XFTY, All Rights Reserved.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * For more information, see the LICENSE file in the root directory.
 */
package com.nameproject.nameproject5At.conf;

import com.nameproject.nameproject5At.NameProjectApplication;
import javafx.application.Platform;
import javafx.scene.control.Alert;
import javafx.scene.control.ButtonType;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.yaml.snakeyaml.Yaml;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Map;
import java.util.Optional;

public class ConfigCreator {
    private static final Logger logger = LogManager.getLogger(ConfigCreator.class);

    public Map<String, Object> getOrCreateConfigFile() {
        try {
            System.out.println(System.getProperty("user.dir"));
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
            if (result.get() == ButtonType.OK) {
                // 文件不存在，创建文件夹
                createFolder(npDir);
                // 创建并写入 YAML 文件
                createYamlFile(configFile);
            } else {
                Platform.exit();
                System.exit(0);
            }

            // 重新读取并返回yaml文件
            return readYamlFile(configFile);

        } catch (Exception e) {
            logger.error("Failed to get or create config file.", e);
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
            logger.error("Failed to read YAML file: " + filePath, e);
            return null;
        }
    }

    private Path getDocumentsDir() {
        // 获取用户主目录
        String userHome = System.getProperty("user.home");
        Path documentsDir;

        if (isWindows()) {
            documentsDir = Paths.get(userHome, "Documents");
        } else {
            documentsDir = Paths.get(userHome, "Documents"); // 根据实际情况修改这里
        }

        logger.debug("Documents directory: " + documentsDir);
        return documentsDir;
    }

    private static boolean isWindows() {
        String os = System.getProperty("os.name").toLowerCase();
        return os.contains("win");
    }

    private static void createFolder(Path folderPath) {
        try {
            Files.createDirectories(folderPath);
            logger.info("Folder created: " + folderPath);
        } catch (IOException e) {
            logger.error("Failed to create folder: " + folderPath, e);
        }
    }

    private static void createYamlFile(Path filePath) {
        try (InputStream inputStream = NameProjectApplication.class.getResourceAsStream("/com/nameproject/nameproject5At/config/modelConfigure.yaml")) {
            if (inputStream == null) {
                throw new IOException("Resource not found: /config/modelConfigure.yaml");
            }
            String yamlData = new String(inputStream.readAllBytes());
            Files.writeString(filePath, yamlData);
            logger.info("YAML file created: " + filePath);
        } catch (IOException e) {
            logger.error("Failed to create YAML file: " + filePath, e);
        }
    }
}
