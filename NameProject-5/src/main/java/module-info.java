module com.nameproject.v5.nameproject5 {
    requires javafx.controls;
    requires javafx.fxml;

    requires org.kordamp.bootstrapfx.core;

    opens com.nameproject.v5.nameproject5 to javafx.fxml;
    exports com.nameproject.v5.nameproject5;
    exports com.nameproject.v5.nameproject5.controller;
}