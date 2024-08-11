package com.nameproject.nameproject5At;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.stage.Stage;
import org.yaml.snakeyaml.Yaml;

import java.io.IOException;
import java.util.Map;

public class NameProjectApplication extends Application {
    @Override
    public void start(Stage stage) throws IOException {

        // 读取 yaml 文件
        Yaml yaml = new Yaml();
        Map<String, Object> sysinfo = yaml.load(NameProjectApplication.class.getResourceAsStream("config/SoftwareInfo.yaml"));

        // 设置 fxml
        FXMLLoader fxmlLoader = new FXMLLoader(NameProjectApplication.class.getResource("mainWindow-classic.fxml"));
        Parent root = fxmlLoader.load();
        Scene scene = new Scene(root, 800, 500);

        // 设置标题
        String title ="NameProject " + sysinfo.get("version").toString();
        stage.setTitle(title);

        stage.setScene(scene);
        stage.show();

        try {
            Label versionLabel = (Label) root.lookup("#version");
            versionLabel.setText("Version: " + sysinfo.get("version").toString());
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    public static void main(String[] args) {
        launch();
    }
}