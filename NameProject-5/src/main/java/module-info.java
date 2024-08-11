module com.nameproject.v5.nameproject5 {
    requires javafx.controls;
    requires javafx.fxml;

    requires org.kordamp.bootstrapfx.core;
    requires org.yaml.snakeyaml;

    opens com.nameproject.nameproject5At to javafx.fxml;
    exports com.nameproject.nameproject5At;
    exports com.nameproject.nameproject5At.controller;
    exports com.nameproject.nameproject5At.flusher;
}