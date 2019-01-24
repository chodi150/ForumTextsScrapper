from functools import reduce

# Mapping of possible month names and abbreviations to their respective values
# Necessary in process of parsing polish dates

class PolishMonthHelper:
    def __init__(self):
        self.months = dict()
        self.months[1] = {"sty", "styczeń", "styczniu", "styczen", "stycznia", "stycz"}
        self.months[2] = {"lut", "luty", "lutego", "lutym"}
        self.months[3] = {"mar", "marzec", "marca", "marcu"}
        self.months[4] = {"kwie", "kwiecień", "kw", "kwietnia", "kwietniu", "kwiecien", "kwi"}
        self.months[5] = {"maj", "maja", "maju"}
        self.months[6] = {"cze", "czer", "czerwiec", "czerwca", "czerwcu", "czerw"}
        self.months[7] = {"lip", "lipiec", "lipca", "lipcu", }
        self.months[8] = {"sie", "sierpień", "sierpnia", "sierpniu", "sierp"}
        self.months[9] = {"wrz", "wrzesień", "wrzesien", "września", "wrześniu", "wrzes"}
        self.months[10] = {"paź", "paz", "październik", "padziernik", "października", "pazdz", "paźdz"}
        self.months[11] = {"lis", "listopad", "listopada", "listopadzie", "listop"}
        self.months[12] = {"gru", "grudzień", "grudzien", "grudnia", "grudniu", "grud", "grudz"}
        self.all_months_abbreviations = reduce(lambda x, y: x | y, list(map(lambda x: x[1], self.months.items())))

    def get_month(self, abbreviation):
        for k, v in self.months.items():
            if abbreviation in v:
                return str(k)
