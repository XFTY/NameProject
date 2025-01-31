package com.nameproject.nameproject5At.conf;

import org.jetbrains.annotations.NotNull;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

public class NameWrapper {
    public boolean checkIfHaveSex(String args) {
        return args.contains("/");
    }

    // 对已有性别的数据进行拆分处理

    /**
     * 功能：对用户在文本框中的一行数据进行程序化转译
     * <p>
     * 注意：需要该数据拥有性别信息(有"/"且/后面为男或女)
     *
     * @param args String 类型，且格式必须为 "姓名/性别"
     * @return Map<String, Boolean> 类型，key为姓名，value为性别。true为男，false为女
     */

    public Map<Map<String, String>, Map<String, Integer>> splitSex(String args) {
        // 创建一个 HashMap
        Map<Map<String, String>, Map<String, Integer>> rmap = new HashMap<>();
        // 拆分输入为一个列表
        List<String> list = List.of(args.split("/"));

        // 判断列表长度是否为2
        if (list.size() == 2) {
            //判断列表第二个元素是否为男或女
            if (Objects.equals(list.get(1), "男")) {
                rmap.put(Map.of("name", list.get(0)), Map.of("sex", 1));
                return rmap;
            } else if (Objects.equals(list.get(1), "女")) {
                rmap.put(Map.of("name", list.get(0)), Map.of("sex", 0));
                return rmap;
            } else {
                // 如果列表第二个元素不为男或女，则返回 null
                rmap.put(Map.of("name", list.get(0)), Map.of("sex", null));
                return rmap;
            }
        } else {
            // 如果列表长度不为2，则返回 null
            return null;
        }
    }
}
