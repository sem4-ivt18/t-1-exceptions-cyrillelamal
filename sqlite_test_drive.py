from json_reader import load_json
from UserORM import User


data = load_json()

conn = User.set_connection('example.db')

# # CREATE TABLE
# User.create_table()

# # INSERT INTO
# for user_data in data:
#     u = User()
#     for col, val in user_data.items():
#         if col == 'id':
#             continue
#         setattr(u, col, val)
#     u.save()

# # SELECT
# for i in range(30, 70):
#     user = User.get_by_pk(i)
#     print(user.__dict__)

# # DELETE
# for i in range(20, 40):
#     user = User.get_by_pk(i)
#     user.delete()


User.close_connection()
