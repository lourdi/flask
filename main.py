from flask import Flask, request, jsonify
import camelot
import os

app = Flask(__name__)

@app.route('/pdf-to-csv', methods=['POST'])
def pdf_to_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        # Save the uploaded PDF file temporarily
        pdf_file_path = 'temp.pdf'
        file.save(pdf_file_path)

        try:
            # Use Camelot-Py to extract tables from the PDF
            tables = camelot.read_pdf(pdf_file_path)

            # Convert each table to CSV
            csv_files = []
            for i, table in enumerate(tables):
                csv_file_path = f'table_{i + 1}.csv'
                table.to_csv(csv_file_path)
                csv_files.append(csv_file_path)

            return jsonify({'success': 'PDF to CSV conversion successful', 'csv_files': csv_files})
        except Exception as e:
            return jsonify({'error': str(e)})
        finally:
            # Remove the temporary PDF file
            os.remove(pdf_file_path)

if __name__ == '__main__':
    app.run(debug=True)

