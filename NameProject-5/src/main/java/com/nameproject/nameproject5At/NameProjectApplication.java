package com.nameproject.nameproject5At;

import com.nameproject.nameproject5At.conf.ConfManager;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.stage.Stage;

import java.io.IOException;
import java.util.Map;

public class NameProjectApplication extends Application {
    private Parent root;

    @Override
    public void start(Stage stage) throws IOException {
        Map<String, Object> sysinfo = ConfManager.ReturnSysInfo();

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

    public static void main(String[] args) {
        launch();
    }

    public Parent getRoot() {
        return root;
    }
}