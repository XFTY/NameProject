module com.nameproject.v5.nameproject5 {
    requires javafx.controls;
    requires javafx.fxml;

    requires org.kordamp.bootstrapfx.core;
    requires org.yaml.snakeyaml;
    requires java.desktop;
    requires java.logging;
    requires org.apache.logging.log4j;

    opens com.nameproject.nameproject5At to javafx.fxml;
    opens com.nameproject.nameproject5At.controller to javafx.fxml;

    exports com.nameproject.nameproject5At;
    exports com.nameproject.nameproject5At.controller;
    exports com.nameproject.nameproject5At.flusher;
    exports com.nameproject.nameproject5At.conf;
    opens com.nameproject.nameproject5At.conf to javafx.fxml;
    exports com.nameproject.nameproject5At.controller.sound;
    opens com.nameproject.nameproject5At.controller.sound to javafx.fxml;
}