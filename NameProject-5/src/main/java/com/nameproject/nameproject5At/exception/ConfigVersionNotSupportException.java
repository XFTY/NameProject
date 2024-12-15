package com.nameproject.nameproject5At.exception;

public class ConfigVersionNotSupportException extends Exception{
    public ConfigVersionNotSupportException(String message) {
        super(message);
    }

    public ConfigVersionNotSupportException(String message, Throwable cause) {
        super(message, cause);
    }
}
