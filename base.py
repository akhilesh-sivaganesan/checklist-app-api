from flask import Flask
from flask import jsonify, request
import os
import sqlalchemy
from sqlalchemy.sql import text
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


host = 'aero-webapps.cnh4wzlssbju.us-gov-west-1.rds.amazonaws.com'
database = 'osf'
username = 'osf_data_team'
password = 'Data4Life135!'
# table = 'sharepoint_db'
port = '5432'
engine = sqlalchemy.create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')
con = engine.connect()


@app.route('/', methods=['GET'])
@cross_origin()
def handle_forms():
    select_query = text('SELECT * FROM osf_public.templates')
    rs = con.execute(select_query)
    rows = rs.fetchall()
    final_result = []
    for r in rows:
        tempDict = dict(r._mapping.items())
        select_query = text('SELECT * FROM osf_public.template_nodes WHERE template_id = ' + "\'" + tempDict['template_id'] + "\'")
        result = con.execute(select_query)
        resultS = result.fetchall()
        tempDict['nodes'] = [dict(t._mapping.items()) for t in resultS]
        final_result.append(tempDict)
    final_response = jsonify(final_result)
    #final_response.headers.add('Access-Control-Allow-Origin', '*')
    return final_response, 200

@app.route('/', methods=['POST'])
@cross_origin()
def create_form_template():
    data = request.get_json(force=True)
    insert_query = text("INSERT INTO osf_public.templates (template_id, template_title, template_owner_id, created_at) VALUES ('% s', '% s', '% s', '% s');" % (data['template_id'], data['template_title'], data['template_owner_id'], data['template_created_at']))
    con.execute(insert_query)

    for ditem in data['template_nodes']:
        insert_query = text("INSERT INTO osf_public.template_nodes (node_id, node_title, node_description, node_type, template_id) VALUES ('%s', '%s', '%s', '%s', '%s');" % (ditem['node_id'], ditem['node_title'], ditem['node_description'], ditem['node_type'], ditem['template_id']))
        con.execute(insert_query)

    commit_text = text("COMMIT;")
    con.execute(commit_text)

    # HTTP 201 Created
    return jsonify({"template_id": data['template_id']}), 201


@app.route('/', methods=['PUT'])
@cross_origin()
def update_form():
    data = request.get_json(force=True)
    host = 'aero-webapps.cnh4wzlssbju.us-gov-west-1.rds.amazonaws.com'
    database = 'osf'
    username = 'osf_data_team'
    password = 'Data4Life135!'
    # table = 'sharepoint_db'
    port = '5432'


    engine = sqlalchemy.create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')

    con = engine.connect()

    for ditem in data['items']:
        update_query = text("UPDATE osf_public.akhilesh_form_items SET description = '%s', completiontimestamp = '%s', completionstatus = '%s' WHERE item_id = '%s';" % (ditem['description'], ditem['completiontimestamp'], ditem['completionstatus'],  ditem['item_id']))
        con.execute(update_query)

    commit_text = text("COMMIT;")
    con.execute(commit_text)


    # HTTP 201 Created
    return jsonify({"form_id": data['id']}), 201



@app.route('/', methods=['DELETE'])
@cross_origin()
def delete_record():
    """Delete Checklist By ID
    @param id: the id
    @return: 204: an empty payload.
    @raise 404: if book request not found
    """
    data = request.get_json(force=True)
    _id = data['id']
    host = 'aero-webapps.cnh4wzlssbju.us-gov-west-1.rds.amazonaws.com'
    database = 'osf'
    username = 'osf_data_team'
    password = 'Data4Life135!'
    # table = 'sharepoint_db'
    port = '5432'

    engine = sqlalchemy.create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')

    con = engine.connect()

    query = text("delete from osf_public.akhilesh_form_items WHERE form_id = " + "\'" + _id + "\'")
    print(query)
    con.execute(query)

    query = text("delete from osf_public.akhilesh_forms WHERE id = " + "\'" + _id + "\'")
    print(query)
    con.execute(query)

    return '', 204


 
# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)