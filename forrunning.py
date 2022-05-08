import main_final

if __name__ == "__main__":
    item_dict = {}

    level15_result = main_final.aggregate_analyze(1000, 6, "MonkeyKing", "MonkeyKing",
                                                  "Monkey King 1st", "King Monkey 2nd", 20, 0, False, item_dict,
                                                  True, False, False, False, False)

    noMKB_result = main_final.aggregate_analyze(1000, 15, "MonkeyKing", "MonkeyKing",
                                                "Monkey King 1st", "King Monkey 2nd", 60, 0, False, item_dict,
                                                True, False, False, False, False)
    # You could try item "Heart" or "Satanic" here.
    item_dict["MKB"] = 1
    MKB_result = main_final.aggregate_analyze(1000, 15, "MonkeyKing", "MonkeyKing",
                                              "Monkey King 1st", "King Monkey 2nd", 60, 0, False, item_dict,
                                              True, False, False, False, False)

    main_final.creat_plot(noMKB_result, MKB_result)
