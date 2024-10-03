package com.nameproject.nameproject5At;

import com.nameproject.nameproject5At.conf.ConfManager;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.ButtonType;
import javafx.scene.control.Label;
import javafx.stage.Stage;

import java.io.IOException;
import java.util.Map;
import java.util.Optional;

public class NameProjectApplication extends Application {
    private Parent root;

    @Override
    public void start(Stage stage) throws IOException {
        System.out.println("Software Start...");
        Map<String, Object> sysinfo = ConfManager.ReturnSysInfo();
        Map<String, Object> usrinfo = ConfManager.ReturnUsrInfo();

        // 设置 fxml
        FXMLLoader fxmlLoader = new FXMLLoader(NameProjectApplication.class.getResource("fxml/mainWindow-classic.fxml"));
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

        // 随机选择欢迎语


        // 监听窗口关闭事件
        stage.setOnCloseRequest(event -> { // 替换为 lambda
            Alert alert = new Alert(Alert.AlertType.CONFIRMATION);
            alert.setTitle("退出程序");

            alert.setHeaderText("您正在尝试退出程序...");
            alert.setContentText("按下“确认”将会立即退出程序，按下“取消”将返回NameProject\n5");

            Optional<ButtonType> result = alert.showAndWait();

            if (result.get() == ButtonType.OK) {
                System.exit(0);// 立刻结束NameProject java线程
            } else {
                event.consume();
            }

        });


        Button stopButton = (Button) root.lookup("#stopButton");
        stopButton.setDisable(true);

    }

    public static void main(String[] args) {
        launch();
    }

    @Deprecated
    public Parent getRoot() {
        return root;
    }
}