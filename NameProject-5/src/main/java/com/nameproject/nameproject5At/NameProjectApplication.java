package com.nameproject.nameproject5At;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.stage.Stage;
import org.yaml.snakeyaml.Yaml;

import java.io.IOException;
import java.util.Map;

public class NameProjectApplication extends Application {

    @Override
    public void start(Stage stage) throws IOException {

        // 读取 yaml 文件
        Map<String, Object> sysinfo = GetSysInfo();
        ConfigCreator configCreator = new ConfigCreator();
        Map<String, Object> configureFile = configCreator.getOrCreateConfigFile();

        // 设置 fxml
        FXMLLoader fxmlLoader = new FXMLLoader(NameProjectApplication.class.getResource("mainWindow-classic.fxml"));
        Parent root = fxmlLoader.load();

        // 设置窗体
        Scene scene = new Scene(root, 800, 500);
        stage.setMinWidth(800);
        stage.setMinHeight(500);

        // 设置标题
        String title ="NameProject " + sysinfo.get("version").toString();
        stage.setTitle(title);

        stage.setScene(scene);
        stage.show();

        // 设置版本号在软件窗口内
        try {
            Label versionLabel = (Label) root.lookup("#versionLabel");
            versionLabel.setText("Version: " + sysinfo.get("version").toString());
        } catch (Exception e) {
            e.printStackTrace();
        }

        Button stopButton = (Button) root.lookup("#stopButton");
        stopButton.setDisable(true);

    }

    public Map<String, Object> GetSysInfo() {
        Yaml yaml = new Yaml();
        Map<String, Object> sysinfo = yaml.load(NameProjectApplication.class.getResourceAsStream("config/SoftwareInfo.yaml"));
        return sysinfo;
    }

    public static void main(String[] args) {
        launch();
    }
}