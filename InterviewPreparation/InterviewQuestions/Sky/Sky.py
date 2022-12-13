import logging
from datetime import date

log = logging.getLogger() 
log.setLevel(logging.INFO) 


class Billing():
    def __init__(self, call_details):
        self.call_details = call_details
        
    def call_cost(self):
        """
        In this function it will calculate the cost of the each call.
        """
        for l in self.call_details:
            dur_hours= l[2].split(':')
            dur_seconds = int(dur_hours[0])*3600+int(dur_hours[1])*60+int(dur_hours[2])
            if dur_seconds > 180:
                cost = (180 * 0.05) + ((dur_seconds - 180) * 0.03)
            else:
                cost = dur_seconds * 0.05
            l.append(cost)
        logging.info(f"Calculated the bill for each call")
        return self.call_details

    def promotional_discount(self, call_details):
        """
        call_details: Input list
        This function returns the user with greatest cost of phone call.
        """
        discount = {}
        for call in call_details:
            if call[0] not in discount:
                discount[call[0]] = call[2]
            elif call[0] in discount and discount[call[0]]< call[2]:
                discount[call[0]] = call[2]
        return discount

    def final_bill(self, call_details, promotion_flag=0):
        """
        call_details: Input list
        promotion_flag: By default promotion flag is 0.
        This function returns the user total bill = actual bill - promotional discount.
        """
        user_bill = Utility.custom_group_by(self, call_details, [0], 2)
        if promotion_flag == 1:
            user_discount = self.promotional_discount(call_details)
            for bill in user_bill:
                if bill[1] - user_discount[bill[0]] > 0:
                    bill[1] -= user_discount[bill[0]]
            logging.info("Promotional discount applied")
        else:
            logging.info("No Promotional discount applied")
        return user_bill


class Utility():
    def custom_group_by(self, List, Keys, Val):
        """
        List: Input List
        Keys: Index of key columns for aggregation.
        Val:  Index of metric column.
        In this function, based on the key column it will give the sum of the Val column.
        It works similar to the group by in rdbms.
        """
        agg_dict = {}
        for row in List:
            key = ''
            for ind in Keys:
                key += row[ind] + ' '
            if key in agg_dict:
                agg_dict[key] += row[Val]
            else:
                agg_dict[key] = row[Val]

        agg_list = []
        for k,v in agg_dict.items():
            temp_list = []
            temp_list.extend(k.strip(' ').split(' '))
            temp_list.append(v)
            agg_list.append(temp_list)
        return agg_list

class File_handling():
    def read_file(self, path, file_name):
        """
        path: file location
        file_name: name of the file
        This function will return the file as nested list
        """
        logging.info(f"Reading the log file from {path}")
        with open(f'{path}/{file_name}') as f:
            bill = f.read().splitlines()
        bill = [line.split(' ') for line in bill]
        return bill

    def file_validation(self, file, file_schema):
        """
        file: Nested list of the input file
        file_schema: Predefined schema of the file
        This function throw an execption if the file is not as expected.
        """
        row_length = file_schema['length']
        try:
            for row in file:
                if len(row) != row_length:
                    raise exception("row length is not as expected, file is corrupted")
                for ind, col in enumerate(row):
                    if len(col) > file_schema['columns'][str(ind)]['length']:
                        raise ValueError("columns length is not as expected, file is corrupted")
        except exception as e:
            print(e)
            sys.exit(1)
        logging.info(f"File is successfully validated")
        return 0 

    def write_file(self, output, path, file_name):
        with open(f'{path}/{file_name}', 'w') as fp:
            for item in output:
                fp.write("%s\n" % ' '.join(map(str, item)))
        logging.info(f'File is successfully written to {path}')   


def main():
    # Creating the file_handing object
    F = File_handling()
    # Reading the call.log file from the directory location
    daily_bill = F.read_file(folder, file_name)
    # Validating the file
    F.file_validation(daily_bill, file_schema)
    # Creating the Billing object to calculate the user bill
    B = Billing(daily_bill)
    # Calculating the cost of each call
    call_cost = B.call_cost()
    # Creating the Utility object for group by function
    U = Utility()
    # Calculating the cost at phone number level
    call_cost = U.custom_group_by(call_cost, [0, 1], 3)
    # Generating the final bill
    output_bill = B.final_bill(call_cost, 1)
    # Writing the final bill to folder location
    F.write_file(output_bill, folder, 'Result.csv')

if __name__ == "__main__":
    folder = '/Users/swaroop/MyNotes/InterviewPreparation/InterviewQuestions/Sky'
    file_name = 'call.log'
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',    
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S', filename=f'billing_{date.today()}.log', force=True)
    file_schema = {
        'length': 3,
        'columns': {
            '0': {
                'length': 5
            },
            '1': {
                'length': 11
            },
            '2': {
                'length': 8 
            }
        }
    }
    main()