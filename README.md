# Distributed KV Store

This repository presents the KeyValueStore_GCP project—a versatile key-value store system implemented using Python 3. The project features a TCP/IP server that seamlessly interacts with clients to execute operations on a robust database. The project incorporates diverse storage options, including native storage using files, integration with Google Cloud Firestore for dynamic NoSQL storage, and Google Cloud Bucket storage for scalable file storage solutions.

## Features

- TCP/IP server for client interaction
- Native storage using files in the 'data' folder
- Google Cloud Firestore integration for NoSQL storage
- Google Cloud Bucket storage for scalable file storage
- Client process for issuing set and get requests
- Workflow automation using the `everything.sh` script

## Getting Started

Follow these instructions to set up and run the KeyValueStore_GCP project on your local machine or Google Cloud environment.

### Prerequisites

- Python 3
- Google Cloud Platform account (for Google Cloud services)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/prashastikarlekar/KeyValueStore_GCP.git
   ```

2. Navigate to the project directory:

   ```bash
   cd KeyValueStore_GCP
   ```

3. Make sure you have the required Python packages installed:

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Place your Google Cloud service account credentials file (`prashasti-karlekar-fall2022-firebase.json`) in the project directory.

## Usage

1. Run the server:

   ```bash
   python server.py
   ```

2. Run the client:

   ```bash
   python client.py
   ```

3. Follow the prompts in the client to perform set and get operations using different storage options.

4. To automate the workflow, run the `everything.sh` script:

   ```bash
   ./everything.sh
   ```

## Operations

The project includes various operations using different storage options, including native storage (file-based), Google Cloud Firestore, and Google Cloud Bucket storage.

1. Native Storage:
   - Data is stored as individual files in the 'data' folder.
   - Perform set and get operations with specified keys and values.
   
2. Google Cloud Firestore:
   - Data is stored in a Firestore collection and document.
   - Set and get operations interact with Firestore for key-value storage.

3. Google Cloud Bucket Storage:
   - Data is stored in a Google Cloud Storage bucket.
   - Create, list, and delete buckets using the script.

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, please submit an issue or a pull request.

---

Feel free to modify and enhance this `README.md` template according to your project's specific details and requirements. Good luck with your KeyValueStore_GCP project!
