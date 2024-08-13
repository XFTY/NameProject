package com.nameproject.nameproject5At.conf;

import com.nameproject.nameproject5At.NameProjectApplication;
import org.yaml.snakeyaml.Yaml;

import java.util.Map;

public class ConfManager {
    // 读取&存储 软件配置 文件
    private static final Map<String, Object> sysinfo = GetSysInfo();
    // 读取&存储 用户配置 文件
    private static final Map<String, Object> usrinfo = GetUsrInfo();

    private static Map<String, Object> GetSysInfo() {
        Yaml yaml = new Yaml();
        Map<String, Object> sysinfo = yaml.load(NameProjectApplication.class.getResourceAsStream("config/SoftwareInfo.yaml"));
        return sysinfo;
    }

    private static Map<String, Object> GetUsrInfo() {
        ConfigCreator configCreator = new ConfigCreator();
        return configCreator.getOrCreateConfigFile();
    }

    public static Map<String, Object> ReturnSysInfo() {
        return sysinfo;
    }

    public static Map<String, Object> ReturnUsrInfo() {
        return usrinfo;
    }
}
