use surrealdb::Surreal;
use surrealdb::opt::auth::Root;
//use surrealdb::sql::Value;
// use surrealdb::engine::remote::ws::Client;
// use surrealdb::engine::remote::ws::Ws;

use surrealdb::engine::remote::http::Client;
use surrealdb::engine::remote::http::Http;
//use std::collections::HashMap;
//use serde_json::Value as JsonValue;
use std::error::Error;
use surrealdb::Response;
//use std::time::Instant;

use pyo3::prelude::*;
//use pyo3::types::PyAny;
use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc, Local, NaiveDate, NaiveDateTime, Duration};
use xlsxwriter::*;

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct AmvStaticInfo {
    pub timestamp: DateTime<Utc>,
    pub ip_address: [u8; 4],
    pub number_of_channels: u8,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct UdpTag40 {
    ip_address: [u8; 4],
    number_of_channels: u8,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct UdpTag49 {
    run_counter: u64,
    len_trigger: u16,
    channel: Vec<u8>,
    peak: Vec<u16>,
    peak_position: Vec<u16>,
    position_over: Vec<u16>,
    position_under: Vec<u16>,
    offset_after: Vec<u16>,
    offset_before: Vec<u16>,
    timestamp: String,
    counter: u64,
    created: String,
}


#[derive(Debug, Serialize, Deserialize)]
pub struct UdpTag41 {
    run_counter: u64,
    channel: Vec<u8>,
    integral: Vec<u64>,
    mass: Vec<u64>,
    offset: Vec<u16>,
    offset1: Vec<u16>,
    offset2: Vec<u16>,
    tolerance_bottom: Vec<u16>,
    tolerance_top: Vec<u16>,
    project: String,
    timestamp: String,
    status: Vec<Vec<String>>,
    counter: u64,
    created: String,
}

#[derive(Debug, Serialize, Deserialize)]
struct RawData {
    run_counter: u64,
    channel: u8,
    data: Vec<i32>,
    timestamp: DateTime<Utc>,
}

// Function to connect to the database
async fn connect_to_db(
    ip: &str,
    port: &str,
    user: &str,
    pw: &str,
    namespace: &str,
    db_name: &str
) -> Result<Surreal<Client>, Box<dyn Error>> {
    //let db = Surreal::new::<Ws>(format!("{}:{}", ip, port)).await?;
    let db = Surreal::new::<Http>(format!("{}:{}", ip, port)).await?;
    db.signin(Root {
        username: &format!("{}", user),
        password: &format!("{}", pw),
    })
    .await?;
    db.use_ns(&format!("{}", namespace)).use_db(&format!("{}", db_name)).await?;
    Ok(db)
}

#[pymodule]
fn sdb_connector(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(select_additional_info_data, m)?)?;
    m.add_function(wrap_pyfunction!(select_measurement_data, m)?)?;
    m.add_function(wrap_pyfunction!(select_raw_data, m)?)?;
    Ok(())
}

#[pyfunction]
fn select_additional_info_data(ip: &str, port: &str,
    user: &str, pw:&str, namespace: &str, db_name: &str,
    table_name: &str, run_id: &str, path_name:&str, select_type: u8) -> PyResult<Vec<(u64, u16, u8, u16, u16, u16, u16, u16, u16, String)>> {
    // Create a Tokio runtime and block on the async function
    let rt = match tokio::runtime::Runtime::new() {
        Ok(rt) => rt,
        Err(e) => {
            println!("Error creating runtime: {:?}", e);
            return Err(PyErr::new::<pyo3::exceptions::PyException, _>("Error creating runtime"));
        }
    };
    let data = match rt.block_on(select_additional_info_data_async(ip, port,user, pw, namespace, db_name, table_name,run_id, path_name, select_type)) {
        Ok(data) => data,
        Err(e) => {
            println!("Error selecting additional info data: {:?}", e);
            return Err(PyErr::new::<pyo3::exceptions::PyException, _>("Error selecting additional info data"));
        }
    };
    Ok(data)
}

#[pyfunction]
fn select_measurement_data(ip: &str, port: &str,
    user: &str, pw:&str, namespace: &str, db_name: &str,
    table_name: &str, run_id: &str, path_name: &str, select_type: u8) -> PyResult<Vec<(u64, u8, u64, u64, u16, u16, u16, u16, u16, String, String, Vec<String>)>> {
    // Create a Tokio runtime and block on the async function
    let rt = match tokio::runtime::Runtime::new() {
        Ok(rt) => rt,
        Err(e) => {
            println!("Error creating runtime: {:?}", e);
            return Err(PyErr::new::<pyo3::exceptions::PyException, _>("Error creating runtime"));
        }
    };
    let data = match rt.block_on(select_measurement_data_async(ip, port,user, pw, namespace, db_name, table_name,run_id, path_name, select_type)) {
        Ok(data) => data,
        Err(e) => {
            println!("Error selecting measurement data: {:?}", e);
            return Err(PyErr::new::<pyo3::exceptions::PyException, _>("Error selecting measurement data"));
        }
    };
    Ok(data)
}

#[pyfunction]
fn select_raw_data(ip: &str, port: &str,
    user: &str, pw:&str, namespace: &str, db_name: &str,
    table_name: &str, run_id: &str) -> PyResult<Vec<(u64, u8, i32, String, u32)>> {
    // Create a Tokio runtime and block on the async function
    let rt = match tokio::runtime::Runtime::new() {
        Ok(rt) => rt,
        Err(e) => {
            println!("Error creating runtime: {:?}", e);
            return Err(PyErr::new::<pyo3::exceptions::PyException, _>("Error creating runtime"));
        }
    };
    let data = match rt.block_on(select_raw_data_async(ip, port,user, pw, namespace, db_name, table_name,run_id)) {
        Ok(data) => data,
        Err(e) => {
            println!("Error selecting raw data: {:?}", e);
            return Err(PyErr::new::<pyo3::exceptions::PyException, _>("Error selecting raw data"));
        }
    };
    Ok(data)
}

// Function to query data and process it
async fn query_additonal_info_data(
    db: &Surreal<Client>,
    table_name: &str,
    run_id: &str
) -> Result<surrealdb::Response, Box<dyn Error>>{
    let result_query = format!(
        "SELECT run_counter, len_trigger, channel, peak, peak_position, position_over, position_under, offset_after, offset_before, timestamp, counter, created FROM {} WHERE run_id = {} ORDER BY run_counter ASC",
        table_name, run_id
    );
    let result = db.query(&result_query).await?;
    Ok(result)
}

pub async fn store_additional_info_data_as_xlsx_1CH(data: &Vec<UdpTag49>,name: &str, ip: &str) -> Result<(), Box<dyn Error>> {
    // Create the workbook and worksheet
    let workbook = Workbook::new(name)?;
    let mut worksheet = workbook.add_worksheet(None)?;

    // Write headers
    let headers = ["Zeitstempel Erstellt", "Sensor IP", "Fortlaufender Zähler", "Zeitstempel Messung", "Highphase Messtrigger",
     "Offset Start CH0", "Offset Ende CH0", "Kurve Start CH0", "Kurve Ende CH0", "Peakwert CH0", "Peakposition CH0",
    ];
    for (col, header) in headers.iter().enumerate() {
        worksheet.write_string(0, col as u16, header, None)?;
    }
    for (i, entry) in data.iter().enumerate() {
        let row = (i + 1) as u32; // Start at the second row
        
        worksheet.write_string(row, 0, &entry.created, None)?;
        worksheet.write_string(row, 1, ip, None)?;
        worksheet.write_number(row, 2, entry.counter as f64, None)?;
        worksheet.write_string(row, 3, &entry.timestamp, None)?;
        worksheet.write_number(row, 4, entry.len_trigger as f64, None)?;
        worksheet.write_number(row, 5, entry.offset_before[0] as f64, None)?;
        worksheet.write_number(row, 6, entry.offset_after[0] as f64, None)?;
        worksheet.write_number(row, 7, entry.position_over[0] as f64, None)?;
        worksheet.write_number(row, 8, entry.position_under[0] as f64, None)?;
        worksheet.write_number(row, 9, entry.peak[0] as f64, None)?;
        worksheet.write_number(row, 10, entry.peak_position[0] as f64, None)?;
    }
    Ok(())
}

pub async fn store_additional_info_data_as_xlsx_2CH(data: &Vec<UdpTag49>,name: &str, ip: &str) -> Result<(), Box<dyn Error>> {
    // Create the workbook and worksheet
    let workbook = Workbook::new(name)?;
    let mut worksheet = workbook.add_worksheet(None)?;

    // Write headers
    let headers = ["Zeitstempel Erstellt", "Sensor IP", "Fortlaufender Zähler", "Zeitstempel Messung", "Highphase Messtrigger",
     "Offset Start CH0", "Offset Ende CH0", "Kurve Start CH0", "Kurve Ende CH0", "Peakwert CH0", "Peakposition CH0",
     "Offset Start CH1", "Offset Ende CH1", "Kurve Start CH1", "Kurve Ende CH1", "Peakwert CH1", "Peakposition CH1",
    ];
    for (col, header) in headers.iter().enumerate() {
        worksheet.write_string(0, col as u16, header, None)?;
    }
    for (i, entry) in data.iter().enumerate() {
        let row = (i + 1) as u32; // Start at the second row
        
        worksheet.write_string(row, 0, &entry.created, None)?;
        worksheet.write_string(row, 1, ip, None)?;
        worksheet.write_number(row, 2, entry.counter as f64, None)?;
        worksheet.write_string(row, 3, &entry.timestamp, None)?;
        worksheet.write_number(row, 4, entry.len_trigger as f64, None)?;

        worksheet.write_number(row, 5, entry.offset_before[0] as f64, None)?;
        worksheet.write_number(row, 6, entry.offset_after[0] as f64, None)?;
        worksheet.write_number(row, 7, entry.position_over[0] as f64, None)?;
        worksheet.write_number(row, 8, entry.position_under[0] as f64, None)?;
        worksheet.write_number(row, 9, entry.peak[0] as f64, None)?;
        worksheet.write_number(row, 10, entry.peak_position[0] as f64, None)?;

        worksheet.write_number(row, 11, entry.offset_before[1] as f64, None)?;
        worksheet.write_number(row, 12, entry.offset_after[1] as f64, None)?;
        worksheet.write_number(row, 13, entry.position_over[1] as f64, None)?;
        worksheet.write_number(row, 14, entry.position_under[1] as f64, None)?;
        worksheet.write_number(row, 15, entry.peak[1] as f64, None)?;
        worksheet.write_number(row, 16, entry.peak_position[1] as f64, None)?;
    }
    Ok(())
}


pub async fn store_additional_info_data_as_xlsx_3CH(data: &Vec<UdpTag49>,name: &str, ip: &str) -> Result<(), Box<dyn Error>> {
    // Create the workbook and worksheet
    let workbook = Workbook::new(name)?;
    let mut worksheet = workbook.add_worksheet(None)?;

    // Write headers
    let headers = ["Zeitstempel Erstellt", "Sensor IP", "Fortlaufender Zähler", "Zeitstempel Messung", "Highphase Messtrigger",
     "Offset Start CH0", "Offset Ende CH0", "Kurve Start CH0", "Kurve Ende CH0", "Peakwert CH0", "Peakposition CH0",
     "Offset Start CH1", "Offset Ende CH1", "Kurve Start CH1", "Kurve Ende CH1", "Peakwert CH1", "Peakposition CH1",
     "Offset Start CH2", "Offset Ende CH2", "Kurve Start CH2", "Kurve Ende CH2", "Peakwert CH2", "Peakposition CH2",
    ];
    for (col, header) in headers.iter().enumerate() {
        worksheet.write_string(0, col as u16, header, None)?;
    }
    for (i, entry) in data.iter().enumerate() {
        let row = (i + 1) as u32; // Start at the second row
        
        worksheet.write_string(row, 0, &entry.created, None)?;
        worksheet.write_string(row, 1, ip, None)?;
        worksheet.write_number(row, 2, entry.counter as f64, None)?;
        worksheet.write_string(row, 3, &entry.timestamp, None)?;
        worksheet.write_number(row, 4, entry.len_trigger as f64, None)?;

        worksheet.write_number(row, 5, entry.offset_before[0] as f64, None)?;
        worksheet.write_number(row, 6, entry.offset_after[0] as f64, None)?;
        worksheet.write_number(row, 7, entry.position_over[0] as f64, None)?;
        worksheet.write_number(row, 8, entry.position_under[0] as f64, None)?;
        worksheet.write_number(row, 9, entry.peak[0] as f64, None)?;
        worksheet.write_number(row, 10, entry.peak_position[0] as f64, None)?;

        worksheet.write_number(row, 11, entry.offset_before[1] as f64, None)?;
        worksheet.write_number(row, 12, entry.offset_after[1] as f64, None)?;
        worksheet.write_number(row, 13, entry.position_over[1] as f64, None)?;
        worksheet.write_number(row, 14, entry.position_under[1] as f64, None)?;
        worksheet.write_number(row, 15, entry.peak[1] as f64, None)?;
        worksheet.write_number(row, 16, entry.peak_position[1] as f64, None)?;


        worksheet.write_number(row, 17, entry.offset_before[2] as f64, None)?;
        worksheet.write_number(row, 18, entry.offset_after[2] as f64, None)?;
        worksheet.write_number(row, 19, entry.position_over[2] as f64, None)?;
        worksheet.write_number(row, 20, entry.position_under[2] as f64, None)?;
        worksheet.write_number(row, 21, entry.peak[2] as f64, None)?;
        worksheet.write_number(row, 22, entry.peak_position[2] as f64, None)?;
    }
    Ok(())
}

pub async fn store_additional_info_data_as_xlsx_4CH(data: &Vec<UdpTag49>,name: &str, ip: &str) -> Result<(), Box<dyn Error>> {
    // Create the workbook and worksheet
    let workbook = Workbook::new(name)?;
    let mut worksheet = workbook.add_worksheet(None)?;

    // Write headers
    let headers = ["Zeitstempel Erstellt", "Sensor IP", "Fortlaufender Zähler", "Zeitstempel Messung", "Highphase Messtrigger",
     "Offset Start CH0", "Offset Ende CH0", "Kurve Start CH0", "Kurve Ende CH0", "Peakwert CH0", "Peakposition CH0",
     "Offset Start CH1", "Offset Ende CH1", "Kurve Start CH1", "Kurve Ende CH1", "Peakwert CH1", "Peakposition CH1",
     "Offset Start CH2", "Offset Ende CH2", "Kurve Start CH2", "Kurve Ende CH2", "Peakwert CH2", "Peakposition CH2",
     "Offset Start CH3", "Offset Ende CH3", "Kurve Start CH3", "Kurve Ende CH3", "Peakwert CH3", "Peakposition CH3",
    ];
    for (col, header) in headers.iter().enumerate() {
        worksheet.write_string(0, col as u16, header, None)?;
    }
    for (i, entry) in data.iter().enumerate() {
        let row = (i + 1) as u32; // Start at the second row
        
        worksheet.write_string(row, 0, &entry.created, None)?;
        worksheet.write_string(row, 1, ip, None)?;
        worksheet.write_number(row, 2, entry.counter as f64, None)?;
        worksheet.write_string(row, 3, &entry.timestamp, None)?;
        worksheet.write_number(row, 4, entry.len_trigger as f64, None)?;

        worksheet.write_number(row, 5, entry.offset_before[0] as f64, None)?;
        worksheet.write_number(row, 6, entry.offset_after[0] as f64, None)?;
        worksheet.write_number(row, 7, entry.position_over[0] as f64, None)?;
        worksheet.write_number(row, 8, entry.position_under[0] as f64, None)?;
        worksheet.write_number(row, 9, entry.peak[0] as f64, None)?;
        worksheet.write_number(row, 10, entry.peak_position[0] as f64, None)?;

        worksheet.write_number(row, 11, entry.offset_before[1] as f64, None)?;
        worksheet.write_number(row, 12, entry.offset_after[1] as f64, None)?;
        worksheet.write_number(row, 13, entry.position_over[1] as f64, None)?;
        worksheet.write_number(row, 14, entry.position_under[1] as f64, None)?;
        worksheet.write_number(row, 15, entry.peak[1] as f64, None)?;
        worksheet.write_number(row, 16, entry.peak_position[1] as f64, None)?;


        worksheet.write_number(row, 17, entry.offset_before[2] as f64, None)?;
        worksheet.write_number(row, 18, entry.offset_after[2] as f64, None)?;
        worksheet.write_number(row, 19, entry.position_over[2] as f64, None)?;
        worksheet.write_number(row, 20, entry.position_under[2] as f64, None)?;
        worksheet.write_number(row, 21, entry.peak[2] as f64, None)?;
        worksheet.write_number(row, 22, entry.peak_position[2] as f64, None)?;

        worksheet.write_number(row, 23, entry.offset_before[3] as f64, None)?;
        worksheet.write_number(row, 24, entry.offset_after[3] as f64, None)?;
        worksheet.write_number(row, 25, entry.position_over[3] as f64, None)?;
        worksheet.write_number(row, 26, entry.position_under[3] as f64, None)?;
        worksheet.write_number(row, 27, entry.peak[3] as f64, None)?;
        worksheet.write_number(row, 28, entry.peak_position[3] as f64, None)?;
    }
    Ok(())
}

pub async fn store_additional_info_data_as_xlsx_5CH(data: &Vec<UdpTag49>,name: &str, ip: &str) -> Result<(), Box<dyn Error>> {
    // Create the workbook and worksheet
    let workbook = Workbook::new(name)?;
    let mut worksheet = workbook.add_worksheet(None)?;

    // Write headers
    let headers = ["Zeitstempel Erstellt", "Sensor IP", "Fortlaufender Zähler", "Zeitstempel Messung", "Highphase Messtrigger",
     "Offset Start CH0", "Offset Ende CH0", "Kurve Start CH0", "Kurve Ende CH0", "Peakwert CH0", "Peakposition CH0",
     "Offset Start CH1", "Offset Ende CH1", "Kurve Start CH1", "Kurve Ende CH1", "Peakwert CH1", "Peakposition CH1",
     "Offset Start CH2", "Offset Ende CH2", "Kurve Start CH2", "Kurve Ende CH2", "Peakwert CH2", "Peakposition CH2",
     "Offset Start CH3", "Offset Ende CH3", "Kurve Start CH3", "Kurve Ende CH3", "Peakwert CH3", "Peakposition CH3",
     "Offset Start CH4", "Offset Ende CH4", "Kurve Start CH4", "Kurve Ende CH4", "Peakwert CH4", "Peakposition CH4",
    ];
    for (col, header) in headers.iter().enumerate() {
        worksheet.write_string(0, col as u16, header, None)?;
    }
    for (i, entry) in data.iter().enumerate() {
        let row = (i + 1) as u32; // Start at the second row
        
        worksheet.write_string(row, 0, &entry.created, None)?;
        worksheet.write_string(row, 1, ip, None)?;
        worksheet.write_number(row, 2, entry.counter as f64, None)?;
        worksheet.write_string(row, 3, &entry.timestamp, None)?;
        worksheet.write_number(row, 4, entry.len_trigger as f64, None)?;

        worksheet.write_number(row, 5, entry.offset_before[0] as f64, None)?;
        worksheet.write_number(row, 6, entry.offset_after[0] as f64, None)?;
        worksheet.write_number(row, 7, entry.position_over[0] as f64, None)?;
        worksheet.write_number(row, 8, entry.position_under[0] as f64, None)?;
        worksheet.write_number(row, 9, entry.peak[0] as f64, None)?;
        worksheet.write_number(row, 10, entry.peak_position[0] as f64, None)?;

        worksheet.write_number(row, 11, entry.offset_before[1] as f64, None)?;
        worksheet.write_number(row, 12, entry.offset_after[1] as f64, None)?;
        worksheet.write_number(row, 13, entry.position_over[1] as f64, None)?;
        worksheet.write_number(row, 14, entry.position_under[1] as f64, None)?;
        worksheet.write_number(row, 15, entry.peak[1] as f64, None)?;
        worksheet.write_number(row, 16, entry.peak_position[1] as f64, None)?;


        worksheet.write_number(row, 17, entry.offset_before[2] as f64, None)?;
        worksheet.write_number(row, 18, entry.offset_after[2] as f64, None)?;
        worksheet.write_number(row, 19, entry.position_over[2] as f64, None)?;
        worksheet.write_number(row, 20, entry.position_under[2] as f64, None)?;
        worksheet.write_number(row, 21, entry.peak[2] as f64, None)?;
        worksheet.write_number(row, 22, entry.peak_position[2] as f64, None)?;

        worksheet.write_number(row, 23, entry.offset_before[3] as f64, None)?;
        worksheet.write_number(row, 24, entry.offset_after[3] as f64, None)?;
        worksheet.write_number(row, 25, entry.position_over[3] as f64, None)?;
        worksheet.write_number(row, 26, entry.position_under[3] as f64, None)?;
        worksheet.write_number(row, 27, entry.peak[3] as f64, None)?;
        worksheet.write_number(row, 28, entry.peak_position[3] as f64, None)?;

        worksheet.write_number(row, 29, entry.offset_before[4] as f64, None)?;
        worksheet.write_number(row, 30, entry.offset_after[4] as f64, None)?;
        worksheet.write_number(row, 31, entry.position_over[4] as f64, None)?;
        worksheet.write_number(row, 32, entry.position_under[4] as f64, None)?;
        worksheet.write_number(row, 33, entry.peak[4] as f64, None)?;
        worksheet.write_number(row, 34, entry.peak_position[4] as f64, None)?;
    }
    Ok(())
}

pub async fn store_additional_info_data_as_xlsx_6CH(data: &Vec<UdpTag49>,name: &str, ip: &str) -> Result<(), Box<dyn Error>> {
    // Create the workbook and worksheet
    let workbook = Workbook::new(name)?;
    let mut worksheet = workbook.add_worksheet(None)?;

    // Write headers
    let headers = ["Zeitstempel Erstellt", "Sensor IP", "Fortlaufender Zähler", "Zeitstempel Messung", "Highphase Messtrigger",
     "Offset Start CH0", "Offset Ende CH0", "Kurve Start CH0", "Kurve Ende CH0", "Peakwert CH0", "Peakposition CH0",
     "Offset Start CH1", "Offset Ende CH1", "Kurve Start CH1", "Kurve Ende CH1", "Peakwert CH1", "Peakposition CH1",
     "Offset Start CH2", "Offset Ende CH2", "Kurve Start CH2", "Kurve Ende CH2", "Peakwert CH2", "Peakposition CH2",
     "Offset Start CH3", "Offset Ende CH3", "Kurve Start CH3", "Kurve Ende CH3", "Peakwert CH3", "Peakposition CH3",
     "Offset Start CH4", "Offset Ende CH4", "Kurve Start CH4", "Kurve Ende CH4", "Peakwert CH4", "Peakposition CH4",
     "Offset Start CH5", "Offset Ende CH5", "Kurve Start CH5", "Kurve Ende CH5", "Peakwert CH5", "Peakposition CH5",
    ];
    for (col, header) in headers.iter().enumerate() {
        worksheet.write_string(0, col as u16, header, None)?;
    }
    for (i, entry) in data.iter().enumerate() {
        let row = (i + 1) as u32; // Start at the second row
        
        worksheet.write_string(row, 0, &entry.created, None)?;
        worksheet.write_string(row, 1, ip, None)?;
        worksheet.write_number(row, 2, entry.counter as f64, None)?;
        worksheet.write_string(row, 3, &entry.timestamp, None)?;
        worksheet.write_number(row, 4, entry.len_trigger as f64, None)?;

        worksheet.write_number(row, 5, entry.offset_before[0] as f64, None)?;
        worksheet.write_number(row, 6, entry.offset_after[0] as f64, None)?;
        worksheet.write_number(row, 7, entry.position_over[0] as f64, None)?;
        worksheet.write_number(row, 8, entry.position_under[0] as f64, None)?;
        worksheet.write_number(row, 9, entry.peak[0] as f64, None)?;
        worksheet.write_number(row, 10, entry.peak_position[0] as f64, None)?;

        worksheet.write_number(row, 11, entry.offset_before[1] as f64, None)?;
        worksheet.write_number(row, 12, entry.offset_after[1] as f64, None)?;
        worksheet.write_number(row, 13, entry.position_over[1] as f64, None)?;
        worksheet.write_number(row, 14, entry.position_under[1] as f64, None)?;
        worksheet.write_number(row, 15, entry.peak[1] as f64, None)?;
        worksheet.write_number(row, 16, entry.peak_position[1] as f64, None)?;


        worksheet.write_number(row, 17, entry.offset_before[2] as f64, None)?;
        worksheet.write_number(row, 18, entry.offset_after[2] as f64, None)?;
        worksheet.write_number(row, 19, entry.position_over[2] as f64, None)?;
        worksheet.write_number(row, 20, entry.position_under[2] as f64, None)?;
        worksheet.write_number(row, 21, entry.peak[2] as f64, None)?;
        worksheet.write_number(row, 22, entry.peak_position[2] as f64, None)?;

        worksheet.write_number(row, 23, entry.offset_before[3] as f64, None)?;
        worksheet.write_number(row, 24, entry.offset_after[3] as f64, None)?;
        worksheet.write_number(row, 25, entry.position_over[3] as f64, None)?;
        worksheet.write_number(row, 26, entry.position_under[3] as f64, None)?;
        worksheet.write_number(row, 27, entry.peak[3] as f64, None)?;
        worksheet.write_number(row, 28, entry.peak_position[3] as f64, None)?;

        worksheet.write_number(row, 29, entry.offset_before[4] as f64, None)?;
        worksheet.write_number(row, 30, entry.offset_after[4] as f64, None)?;
        worksheet.write_number(row, 31, entry.position_over[4] as f64, None)?;
        worksheet.write_number(row, 32, entry.position_under[4] as f64, None)?;
        worksheet.write_number(row, 33, entry.peak[4] as f64, None)?;
        worksheet.write_number(row, 34, entry.peak_position[4] as f64, None)?;

        worksheet.write_number(row, 35, entry.offset_before[5] as f64, None)?;
        worksheet.write_number(row, 36, entry.offset_after[5] as f64, None)?;
        worksheet.write_number(row, 37, entry.position_over[5] as f64, None)?;
        worksheet.write_number(row, 38, entry.position_under[5] as f64, None)?;
        worksheet.write_number(row, 39, entry.peak[5] as f64, None)?;
        worksheet.write_number(row, 40, entry.peak_position[5] as f64, None)?;
    }
    Ok(())
}

pub async fn store_additional_info_data_as_xlsx_7CH(data: &Vec<UdpTag49>,name: &str, ip: &str) -> Result<(), Box<dyn Error>> {
    // Create the workbook and worksheet
    let workbook = Workbook::new(name)?;
    let mut worksheet = workbook.add_worksheet(None)?;

    // Write headers
    let headers = ["Zeitstempel Erstellt", "Sensor IP", "Fortlaufender Zähler", "Zeitstempel Messung", "Highphase Messtrigger",
     "Offset Start CH0", "Offset Ende CH0", "Kurve Start CH0", "Kurve Ende CH0", "Peakwert CH0", "Peakposition CH0",
     "Offset Start CH1", "Offset Ende CH1", "Kurve Start CH1", "Kurve Ende CH1", "Peakwert CH1", "Peakposition CH1",
     "Offset Start CH2", "Offset Ende CH2", "Kurve Start CH2", "Kurve Ende CH2", "Peakwert CH2", "Peakposition CH2",
     "Offset Start CH3", "Offset Ende CH3", "Kurve Start CH3", "Kurve Ende CH3", "Peakwert CH3", "Peakposition CH3",
     "Offset Start CH4", "Offset Ende CH4", "Kurve Start CH4", "Kurve Ende CH4", "Peakwert CH4", "Peakposition CH4",
     "Offset Start CH5", "Offset Ende CH5", "Kurve Start CH5", "Kurve Ende CH5", "Peakwert CH5", "Peakposition CH5",
     "Offset Start CH6", "Offset Ende CH6", "Kurve Start CH6", "Kurve Ende CH6", "Peakwert CH6", "Peakposition CH6",
    ];
    for (col, header) in headers.iter().enumerate() {
        worksheet.write_string(0, col as u16, header, None)?;
    }
    for (i, entry) in data.iter().enumerate() {
        let row = (i + 1) as u32; // Start at the second row
        
        worksheet.write_string(row, 0, &entry.created, None)?;
        worksheet.write_string(row, 1, ip, None)?;
        worksheet.write_number(row, 2, entry.counter as f64, None)?;
        worksheet.write_string(row, 3, &entry.timestamp, None)?;
        worksheet.write_number(row, 4, entry.len_trigger as f64, None)?;

        worksheet.write_number(row, 5, entry.offset_before[0] as f64, None)?;
        worksheet.write_number(row, 6, entry.offset_after[0] as f64, None)?;
        worksheet.write_number(row, 7, entry.position_over[0] as f64, None)?;
        worksheet.write_number(row, 8, entry.position_under[0] as f64, None)?;
        worksheet.write_number(row, 9, entry.peak[0] as f64, None)?;
        worksheet.write_number(row, 10, entry.peak_position[0] as f64, None)?;

        worksheet.write_number(row, 11, entry.offset_before[1] as f64, None)?;
        worksheet.write_number(row, 12, entry.offset_after[1] as f64, None)?;
        worksheet.write_number(row, 13, entry.position_over[1] as f64, None)?;
        worksheet.write_number(row, 14, entry.position_under[1] as f64, None)?;
        worksheet.write_number(row, 15, entry.peak[1] as f64, None)?;
        worksheet.write_number(row, 16, entry.peak_position[1] as f64, None)?;


        worksheet.write_number(row, 17, entry.offset_before[2] as f64, None)?;
        worksheet.write_number(row, 18, entry.offset_after[2] as f64, None)?;
        worksheet.write_number(row, 19, entry.position_over[2] as f64, None)?;
        worksheet.write_number(row, 20, entry.position_under[2] as f64, None)?;
        worksheet.write_number(row, 21, entry.peak[2] as f64, None)?;
        worksheet.write_number(row, 22, entry.peak_position[2] as f64, None)?;

        worksheet.write_number(row, 23, entry.offset_before[3] as f64, None)?;
        worksheet.write_number(row, 24, entry.offset_after[3] as f64, None)?;
        worksheet.write_number(row, 25, entry.position_over[3] as f64, None)?;
        worksheet.write_number(row, 26, entry.position_under[3] as f64, None)?;
        worksheet.write_number(row, 27, entry.peak[3] as f64, None)?;
        worksheet.write_number(row, 28, entry.peak_position[3] as f64, None)?;

        worksheet.write_number(row, 29, entry.offset_before[4] as f64, None)?;
        worksheet.write_number(row, 30, entry.offset_after[4] as f64, None)?;
        worksheet.write_number(row, 31, entry.position_over[4] as f64, None)?;
        worksheet.write_number(row, 32, entry.position_under[4] as f64, None)?;
        worksheet.write_number(row, 33, entry.peak[4] as f64, None)?;
        worksheet.write_number(row, 34, entry.peak_position[4] as f64, None)?;

        worksheet.write_number(row, 35, entry.offset_before[5] as f64, None)?;
        worksheet.write_number(row, 36, entry.offset_after[5] as f64, None)?;
        worksheet.write_number(row, 37, entry.position_over[5] as f64, None)?;
        worksheet.write_number(row, 38, entry.position_under[5] as f64, None)?;
        worksheet.write_number(row, 39, entry.peak[5] as f64, None)?;
        worksheet.write_number(row, 40, entry.peak_position[5] as f64, None)?;

        worksheet.write_number(row, 41, entry.offset_before[6] as f64, None)?;
        worksheet.write_number(row, 42, entry.offset_after[6] as f64, None)?;
        worksheet.write_number(row, 43, entry.position_over[6] as f64, None)?;
        worksheet.write_number(row, 44, entry.position_under[6] as f64, None)?;
        worksheet.write_number(row, 45, entry.peak[6] as f64, None)?;
        worksheet.write_number(row, 46, entry.peak_position[6] as f64, None)?;
    }
    Ok(())
}

pub async fn store_additional_info_data_as_xlsx_8CH(data: &Vec<UdpTag49>,name: &str, ip: &str) -> Result<(), Box<dyn Error>> {
    // Create the workbook and worksheet
    let workbook = Workbook::new(name)?;
    let mut worksheet = workbook.add_worksheet(None)?;

    // Write headers
    let headers = ["Zeitstempel Erstellt", "Sensor IP", "Fortlaufender Zähler", "Zeitstempel Messung", "Highphase Messtrigger",
     "Offset Start CH0", "Offset Ende CH0", "Kurve Start CH0", "Kurve Ende CH0", "Peakwert CH0", "Peakposition CH0",
     "Offset Start CH1", "Offset Ende CH1", "Kurve Start CH1", "Kurve Ende CH1", "Peakwert CH1", "Peakposition CH1",
     "Offset Start CH2", "Offset Ende CH2", "Kurve Start CH2", "Kurve Ende CH2", "Peakwert CH2", "Peakposition CH2",
     "Offset Start CH3", "Offset Ende CH3", "Kurve Start CH3", "Kurve Ende CH3", "Peakwert CH3", "Peakposition CH3",
     "Offset Start CH4", "Offset Ende CH4", "Kurve Start CH4", "Kurve Ende CH4", "Peakwert CH4", "Peakposition CH4",
     "Offset Start CH5", "Offset Ende CH5", "Kurve Start CH5", "Kurve Ende CH5", "Peakwert CH5", "Peakposition CH5",
     "Offset Start CH6", "Offset Ende CH6", "Kurve Start CH6", "Kurve Ende CH6", "Peakwert CH6", "Peakposition CH6",
     "Offset Start CH7", "Offset Ende CH7", "Kurve Start CH7", "Kurve Ende CH7", "Peakwert CH7", "Peakposition CH7",
    ];
    for (col, header) in headers.iter().enumerate() {
        worksheet.write_string(0, col as u16, header, None)?;
    }
    for (i, entry) in data.iter().enumerate() {
        let row = (i + 1) as u32; // Start at the second row
        
        worksheet.write_string(row, 0, &entry.created, None)?;
        worksheet.write_string(row, 1, ip, None)?;
        worksheet.write_number(row, 2, entry.counter as f64, None)?;
        worksheet.write_string(row, 3, &entry.timestamp, None)?;
        worksheet.write_number(row, 4, entry.len_trigger as f64, None)?;

        worksheet.write_number(row, 5, entry.offset_before[0] as f64, None)?;
        worksheet.write_number(row, 6, entry.offset_after[0] as f64, None)?;
        worksheet.write_number(row, 7, entry.position_over[0] as f64, None)?;
        worksheet.write_number(row, 8, entry.position_under[0] as f64, None)?;
        worksheet.write_number(row, 9, entry.peak[0] as f64, None)?;
        worksheet.write_number(row, 10, entry.peak_position[0] as f64, None)?;

        worksheet.write_number(row, 11, entry.offset_before[1] as f64, None)?;
        worksheet.write_number(row, 12, entry.offset_after[1] as f64, None)?;
        worksheet.write_number(row, 13, entry.position_over[1] as f64, None)?;
        worksheet.write_number(row, 14, entry.position_under[1] as f64, None)?;
        worksheet.write_number(row, 15, entry.peak[1] as f64, None)?;
        worksheet.write_number(row, 16, entry.peak_position[1] as f64, None)?;


        worksheet.write_number(row, 17, entry.offset_before[2] as f64, None)?;
        worksheet.write_number(row, 18, entry.offset_after[2] as f64, None)?;
        worksheet.write_number(row, 19, entry.position_over[2] as f64, None)?;
        worksheet.write_number(row, 20, entry.position_under[2] as f64, None)?;
        worksheet.write_number(row, 21, entry.peak[2] as f64, None)?;
        worksheet.write_number(row, 22, entry.peak_position[2] as f64, None)?;

        worksheet.write_number(row, 23, entry.offset_before[3] as f64, None)?;
        worksheet.write_number(row, 24, entry.offset_after[3] as f64, None)?;
        worksheet.write_number(row, 25, entry.position_over[3] as f64, None)?;
        worksheet.write_number(row, 26, entry.position_under[3] as f64, None)?;
        worksheet.write_number(row, 27, entry.peak[3] as f64, None)?;
        worksheet.write_number(row, 28, entry.peak_position[3] as f64, None)?;

        worksheet.write_number(row, 29, entry.offset_before[4] as f64, None)?;
        worksheet.write_number(row, 30, entry.offset_after[4] as f64, None)?;
        worksheet.write_number(row, 31, entry.position_over[4] as f64, None)?;
        worksheet.write_number(row, 32, entry.position_under[4] as f64, None)?;
        worksheet.write_number(row, 33, entry.peak[4] as f64, None)?;
        worksheet.write_number(row, 34, entry.peak_position[4] as f64, None)?;

        worksheet.write_number(row, 35, entry.offset_before[5] as f64, None)?;
        worksheet.write_number(row, 36, entry.offset_after[5] as f64, None)?;
        worksheet.write_number(row, 37, entry.position_over[5] as f64, None)?;
        worksheet.write_number(row, 38, entry.position_under[5] as f64, None)?;
        worksheet.write_number(row, 39, entry.peak[5] as f64, None)?;
        worksheet.write_number(row, 40, entry.peak_position[5] as f64, None)?;

        worksheet.write_number(row, 41, entry.offset_before[6] as f64, None)?;
        worksheet.write_number(row, 42, entry.offset_after[6] as f64, None)?;
        worksheet.write_number(row, 43, entry.position_over[6] as f64, None)?;
        worksheet.write_number(row, 44, entry.position_under[6] as f64, None)?;
        worksheet.write_number(row, 45, entry.peak[6] as f64, None)?;
        worksheet.write_number(row, 46, entry.peak_position[6] as f64, None)?;
        
        worksheet.write_number(row, 47, entry.offset_before[7] as f64, None)?;
        worksheet.write_number(row, 48, entry.offset_after[7] as f64, None)?;
        worksheet.write_number(row, 49, entry.position_over[7] as f64, None)?;
        worksheet.write_number(row, 50, entry.position_under[7] as f64, None)?;
        worksheet.write_number(row, 51, entry.peak[7] as f64, None)?;
        worksheet.write_number(row, 52, entry.peak_position[7] as f64, None)?;
    }
    Ok(())
}

pub async fn store_additional_info_data_as_xlsx_9CH(data: &Vec<UdpTag49>,name: &str, ip: &str) -> Result<(), Box<dyn Error>> {
    // Create the workbook and worksheet
    let workbook = Workbook::new(name)?;
    let mut worksheet = workbook.add_worksheet(None)?;

    // Write headers
    let headers = ["Zeitstempel Erstellt", "Sensor IP", "Fortlaufender Zähler", "Zeitstempel Messung", "Highphase Messtrigger",
     "Offset Start CH0", "Offset Ende CH0", "Kurve Start CH0", "Kurve Ende CH0", "Peakwert CH0", "Peakposition CH0",
     "Offset Start CH1", "Offset Ende CH1", "Kurve Start CH1", "Kurve Ende CH1", "Peakwert CH1", "Peakposition CH1",
     "Offset Start CH2", "Offset Ende CH2", "Kurve Start CH2", "Kurve Ende CH2", "Peakwert CH2", "Peakposition CH2",
     "Offset Start CH3", "Offset Ende CH3", "Kurve Start CH3", "Kurve Ende CH3", "Peakwert CH3", "Peakposition CH3",
     "Offset Start CH4", "Offset Ende CH4", "Kurve Start CH4", "Kurve Ende CH4", "Peakwert CH4", "Peakposition CH4",
     "Offset Start CH5", "Offset Ende CH5", "Kurve Start CH5", "Kurve Ende CH5", "Peakwert CH5", "Peakposition CH5",
     "Offset Start CH6", "Offset Ende CH6", "Kurve Start CH6", "Kurve Ende CH6", "Peakwert CH6", "Peakposition CH6",
     "Offset Start CH7", "Offset Ende CH7", "Kurve Start CH7", "Kurve Ende CH7", "Peakwert CH7", "Peakposition CH7",
    "Offset Start CH8", "Offset Ende CH8", "Kurve Start CH8", "Kurve Ende CH8", "Peakwert CH8", "Peakposition CH8",
    ];
    for (col, header) in headers.iter().enumerate() {
        worksheet.write_string(0, col as u16, header, None)?;
    }
    for (i, entry) in data.iter().enumerate() {
        let row = (i + 1) as u32; // Start at the second row
        
        worksheet.write_string(row, 0, &entry.created, None)?;
        worksheet.write_string(row, 1, ip, None)?;
        worksheet.write_number(row, 2, entry.counter as f64, None)?;
        worksheet.write_string(row, 3, &entry.timestamp, None)?;
        worksheet.write_number(row, 4, entry.len_trigger as f64, None)?;

        worksheet.write_number(row, 5, entry.offset_before[0] as f64, None)?;
        worksheet.write_number(row, 6, entry.offset_after[0] as f64, None)?;
        worksheet.write_number(row, 7, entry.position_over[0] as f64, None)?;
        worksheet.write_number(row, 8, entry.position_under[0] as f64, None)?;
        worksheet.write_number(row, 9, entry.peak[0] as f64, None)?;
        worksheet.write_number(row, 10, entry.peak_position[0] as f64, None)?;

        worksheet.write_number(row, 11, entry.offset_before[1] as f64, None)?;
        worksheet.write_number(row, 12, entry.offset_after[1] as f64, None)?;
        worksheet.write_number(row, 13, entry.position_over[1] as f64, None)?;
        worksheet.write_number(row, 14, entry.position_under[1] as f64, None)?;
        worksheet.write_number(row, 15, entry.peak[1] as f64, None)?;
        worksheet.write_number(row, 16, entry.peak_position[1] as f64, None)?;


        worksheet.write_number(row, 17, entry.offset_before[2] as f64, None)?;
        worksheet.write_number(row, 18, entry.offset_after[2] as f64, None)?;
        worksheet.write_number(row, 19, entry.position_over[2] as f64, None)?;
        worksheet.write_number(row, 20, entry.position_under[2] as f64, None)?;
        worksheet.write_number(row, 21, entry.peak[2] as f64, None)?;
        worksheet.write_number(row, 22, entry.peak_position[2] as f64, None)?;

        worksheet.write_number(row, 23, entry.offset_before[3] as f64, None)?;
        worksheet.write_number(row, 24, entry.offset_after[3] as f64, None)?;
        worksheet.write_number(row, 25, entry.position_over[3] as f64, None)?;
        worksheet.write_number(row, 26, entry.position_under[3] as f64, None)?;
        worksheet.write_number(row, 27, entry.peak[3] as f64, None)?;
        worksheet.write_number(row, 28, entry.peak_position[3] as f64, None)?;

        worksheet.write_number(row, 29, entry.offset_before[4] as f64, None)?;
        worksheet.write_number(row, 30, entry.offset_after[4] as f64, None)?;
        worksheet.write_number(row, 31, entry.position_over[4] as f64, None)?;
        worksheet.write_number(row, 32, entry.position_under[4] as f64, None)?;
        worksheet.write_number(row, 33, entry.peak[4] as f64, None)?;
        worksheet.write_number(row, 34, entry.peak_position[4] as f64, None)?;

        worksheet.write_number(row, 35, entry.offset_before[5] as f64, None)?;
        worksheet.write_number(row, 36, entry.offset_after[5] as f64, None)?;
        worksheet.write_number(row, 37, entry.position_over[5] as f64, None)?;
        worksheet.write_number(row, 38, entry.position_under[5] as f64, None)?;
        worksheet.write_number(row, 39, entry.peak[5] as f64, None)?;
        worksheet.write_number(row, 40, entry.peak_position[5] as f64, None)?;

        worksheet.write_number(row, 41, entry.offset_before[6] as f64, None)?;
        worksheet.write_number(row, 42, entry.offset_after[6] as f64, None)?;
        worksheet.write_number(row, 43, entry.position_over[6] as f64, None)?;
        worksheet.write_number(row, 44, entry.position_under[6] as f64, None)?;
        worksheet.write_number(row, 45, entry.peak[6] as f64, None)?;
        worksheet.write_number(row, 46, entry.peak_position[6] as f64, None)?;
        
        worksheet.write_number(row, 47, entry.offset_before[7] as f64, None)?;
        worksheet.write_number(row, 48, entry.offset_after[7] as f64, None)?;
        worksheet.write_number(row, 49, entry.position_over[7] as f64, None)?;
        worksheet.write_number(row, 50, entry.position_under[7] as f64, None)?;
        worksheet.write_number(row, 51, entry.peak[7] as f64, None)?;
        worksheet.write_number(row, 52, entry.peak_position[7] as f64, None)?;

        worksheet.write_number(row, 53, entry.offset_before[8] as f64, None)?;
        worksheet.write_number(row, 54, entry.offset_after[8] as f64, None)?;
        worksheet.write_number(row, 55, entry.position_over[8] as f64, None)?;
        worksheet.write_number(row, 56, entry.position_under[8] as f64, None)?;
        worksheet.write_number(row, 57, entry.peak[8] as f64, None)?;
        worksheet.write_number(row, 58, entry.peak_position[8] as f64, None)?;
    }
    Ok(())
}

pub async fn store_additional_info_data_as_xlsx_10CH(data: &Vec<UdpTag49>,name: &str, ip: &str) -> Result<(), Box<dyn Error>> {
    // Create the workbook and worksheet
    let workbook = Workbook::new(name)?;
    let mut worksheet = workbook.add_worksheet(None)?;

    // Write headers
    let headers = ["Zeitstempel Erstellt", "Sensor IP", "Fortlaufender Zähler", "Zeitstempel Messung", "Highphase Messtrigger",
     "Offset Start CH0", "Offset Ende CH0", "Kurve Start CH0", "Kurve Ende CH0", "Peakwert CH0", "Peakposition CH0",
     "Offset Start CH1", "Offset Ende CH1", "Kurve Start CH1", "Kurve Ende CH1", "Peakwert CH1", "Peakposition CH1",
     "Offset Start CH2", "Offset Ende CH2", "Kurve Start CH2", "Kurve Ende CH2", "Peakwert CH2", "Peakposition CH2",
     "Offset Start CH3", "Offset Ende CH3", "Kurve Start CH3", "Kurve Ende CH3", "Peakwert CH3", "Peakposition CH3",
     "Offset Start CH4", "Offset Ende CH4", "Kurve Start CH4", "Kurve Ende CH4", "Peakwert CH4", "Peakposition CH4",
     "Offset Start CH5", "Offset Ende CH5", "Kurve Start CH5", "Kurve Ende CH5", "Peakwert CH5", "Peakposition CH5",
     "Offset Start CH6", "Offset Ende CH6", "Kurve Start CH6", "Kurve Ende CH6", "Peakwert CH6", "Peakposition CH6",
     "Offset Start CH7", "Offset Ende CH7", "Kurve Start CH7", "Kurve Ende CH7", "Peakwert CH7", "Peakposition CH7",
    "Offset Start CH8", "Offset Ende CH8", "Kurve Start CH8", "Kurve Ende CH8", "Peakwert CH8", "Peakposition CH8",
    "Offset Start CH9", "Offset Ende CH9", "Kurve Start CH9", "Kurve Ende CH9", "Peakwert CH9", "Peakposition CH9",
    ];
    for (col, header) in headers.iter().enumerate() {
        worksheet.write_string(0, col as u16, header, None)?;
    }
    for (i, entry) in data.iter().enumerate() {
        let row = (i + 1) as u32; // Start at the second row
        
        worksheet.write_string(row, 0, &entry.created, None)?;
        worksheet.write_string(row, 1, ip, None)?;
        worksheet.write_number(row, 2, entry.counter as f64, None)?;
        worksheet.write_string(row, 3, &entry.timestamp, None)?;
        worksheet.write_number(row, 4, entry.len_trigger as f64, None)?;

        worksheet.write_number(row, 5, entry.offset_before[0] as f64, None)?;
        worksheet.write_number(row, 6, entry.offset_after[0] as f64, None)?;
        worksheet.write_number(row, 7, entry.position_over[0] as f64, None)?;
        worksheet.write_number(row, 8, entry.position_under[0] as f64, None)?;
        worksheet.write_number(row, 9, entry.peak[0] as f64, None)?;
        worksheet.write_number(row, 10, entry.peak_position[0] as f64, None)?;

        worksheet.write_number(row, 11, entry.offset_before[1] as f64, None)?;
        worksheet.write_number(row, 12, entry.offset_after[1] as f64, None)?;
        worksheet.write_number(row, 13, entry.position_over[1] as f64, None)?;
        worksheet.write_number(row, 14, entry.position_under[1] as f64, None)?;
        worksheet.write_number(row, 15, entry.peak[1] as f64, None)?;
        worksheet.write_number(row, 16, entry.peak_position[1] as f64, None)?;


        worksheet.write_number(row, 17, entry.offset_before[2] as f64, None)?;
        worksheet.write_number(row, 18, entry.offset_after[2] as f64, None)?;
        worksheet.write_number(row, 19, entry.position_over[2] as f64, None)?;
        worksheet.write_number(row, 20, entry.position_under[2] as f64, None)?;
        worksheet.write_number(row, 21, entry.peak[2] as f64, None)?;
        worksheet.write_number(row, 22, entry.peak_position[2] as f64, None)?;

        worksheet.write_number(row, 23, entry.offset_before[3] as f64, None)?;
        worksheet.write_number(row, 24, entry.offset_after[3] as f64, None)?;
        worksheet.write_number(row, 25, entry.position_over[3] as f64, None)?;
        worksheet.write_number(row, 26, entry.position_under[3] as f64, None)?;
        worksheet.write_number(row, 27, entry.peak[3] as f64, None)?;
        worksheet.write_number(row, 28, entry.peak_position[3] as f64, None)?;

        worksheet.write_number(row, 29, entry.offset_before[4] as f64, None)?;
        worksheet.write_number(row, 30, entry.offset_after[4] as f64, None)?;
        worksheet.write_number(row, 31, entry.position_over[4] as f64, None)?;
        worksheet.write_number(row, 32, entry.position_under[4] as f64, None)?;
        worksheet.write_number(row, 33, entry.peak[4] as f64, None)?;
        worksheet.write_number(row, 34, entry.peak_position[4] as f64, None)?;

        worksheet.write_number(row, 35, entry.offset_before[5] as f64, None)?;
        worksheet.write_number(row, 36, entry.offset_after[5] as f64, None)?;
        worksheet.write_number(row, 37, entry.position_over[5] as f64, None)?;
        worksheet.write_number(row, 38, entry.position_under[5] as f64, None)?;
        worksheet.write_number(row, 39, entry.peak[5] as f64, None)?;
        worksheet.write_number(row, 40, entry.peak_position[5] as f64, None)?;

        worksheet.write_number(row, 41, entry.offset_before[6] as f64, None)?;
        worksheet.write_number(row, 42, entry.offset_after[6] as f64, None)?;
        worksheet.write_number(row, 43, entry.position_over[6] as f64, None)?;
        worksheet.write_number(row, 44, entry.position_under[6] as f64, None)?;
        worksheet.write_number(row, 45, entry.peak[6] as f64, None)?;
        worksheet.write_number(row, 46, entry.peak_position[6] as f64, None)?;
        
        worksheet.write_number(row, 47, entry.offset_before[7] as f64, None)?;
        worksheet.write_number(row, 48, entry.offset_after[7] as f64, None)?;
        worksheet.write_number(row, 49, entry.position_over[7] as f64, None)?;
        worksheet.write_number(row, 50, entry.position_under[7] as f64, None)?;
        worksheet.write_number(row, 51, entry.peak[7] as f64, None)?;
        worksheet.write_number(row, 52, entry.peak_position[7] as f64, None)?;

        worksheet.write_number(row, 53, entry.offset_before[8] as f64, None)?;
        worksheet.write_number(row, 54, entry.offset_after[8] as f64, None)?;
        worksheet.write_number(row, 55, entry.position_over[8] as f64, None)?;
        worksheet.write_number(row, 56, entry.position_under[8] as f64, None)?;
        worksheet.write_number(row, 57, entry.peak[8] as f64, None)?;
        worksheet.write_number(row, 58, entry.peak_position[8] as f64, None)?;

        worksheet.write_number(row, 59, entry.offset_before[9] as f64, None)?;
        worksheet.write_number(row, 60, entry.offset_after[9] as f64, None)?;
        worksheet.write_number(row, 61, entry.position_over[9] as f64, None)?;
        worksheet.write_number(row, 62, entry.position_under[9] as f64, None)?;
        worksheet.write_number(row, 63, entry.peak[9] as f64, None)?;
        worksheet.write_number(row, 64, entry.peak_position[9] as f64, None)?;
    }
    Ok(())
}

pub async fn store_additional_info_data_as_xlsx_11CH(data: &Vec<UdpTag49>,name: &str, ip: &str) -> Result<(), Box<dyn Error>> {
    // Create the workbook and worksheet
    let workbook = Workbook::new(name)?;
    let mut worksheet = workbook.add_worksheet(None)?;

    // Write headers
    let headers = ["Zeitstempel Erstellt", "Sensor IP", "Fortlaufender Zähler", "Zeitstempel Messung", "Highphase Messtrigger",
     "Offset Start CH0", "Offset Ende CH0", "Kurve Start CH0", "Kurve Ende CH0", "Peakwert CH0", "Peakposition CH0",
     "Offset Start CH1", "Offset Ende CH1", "Kurve Start CH1", "Kurve Ende CH1", "Peakwert CH1", "Peakposition CH1",
     "Offset Start CH2", "Offset Ende CH2", "Kurve Start CH2", "Kurve Ende CH2", "Peakwert CH2", "Peakposition CH2",
     "Offset Start CH3", "Offset Ende CH3", "Kurve Start CH3", "Kurve Ende CH3", "Peakwert CH3", "Peakposition CH3",
     "Offset Start CH4", "Offset Ende CH4", "Kurve Start CH4", "Kurve Ende CH4", "Peakwert CH4", "Peakposition CH4",
     "Offset Start CH5", "Offset Ende CH5", "Kurve Start CH5", "Kurve Ende CH5", "Peakwert CH5", "Peakposition CH5",
     "Offset Start CH6", "Offset Ende CH6", "Kurve Start CH6", "Kurve Ende CH6", "Peakwert CH6", "Peakposition CH6",
     "Offset Start CH7", "Offset Ende CH7", "Kurve Start CH7", "Kurve Ende CH7", "Peakwert CH7", "Peakposition CH7",
    "Offset Start CH8", "Offset Ende CH8", "Kurve Start CH8", "Kurve Ende CH8", "Peakwert CH8", "Peakposition CH8",
    "Offset Start CH9", "Offset Ende CH9", "Kurve Start CH9", "Kurve Ende CH9", "Peakwert CH9", "Peakposition CH9",
    "Offset Start CH10", "Offset Ende CH10", "Kurve Start CH10", "Kurve Ende CH10", "Peakwert CH10", "Peakposition CH10",
    
    ];
    for (col, header) in headers.iter().enumerate() {
        worksheet.write_string(0, col as u16, header, None)?;
    }
    for (i, entry) in data.iter().enumerate() {
        let row = (i + 1) as u32; // Start at the second row
        
        worksheet.write_string(row, 0, &entry.created, None)?;
        worksheet.write_string(row, 1, ip, None)?;
        worksheet.write_number(row, 2, entry.counter as f64, None)?;
        worksheet.write_string(row, 3, &entry.timestamp, None)?;
        worksheet.write_number(row, 4, entry.len_trigger as f64, None)?;

        worksheet.write_number(row, 5, entry.offset_before[0] as f64, None)?;
        worksheet.write_number(row, 6, entry.offset_after[0] as f64, None)?;
        worksheet.write_number(row, 7, entry.position_over[0] as f64, None)?;
        worksheet.write_number(row, 8, entry.position_under[0] as f64, None)?;
        worksheet.write_number(row, 9, entry.peak[0] as f64, None)?;
        worksheet.write_number(row, 10, entry.peak_position[0] as f64, None)?;

        worksheet.write_number(row, 11, entry.offset_before[1] as f64, None)?;
        worksheet.write_number(row, 12, entry.offset_after[1] as f64, None)?;
        worksheet.write_number(row, 13, entry.position_over[1] as f64, None)?;
        worksheet.write_number(row, 14, entry.position_under[1] as f64, None)?;
        worksheet.write_number(row, 15, entry.peak[1] as f64, None)?;
        worksheet.write_number(row, 16, entry.peak_position[1] as f64, None)?;


        worksheet.write_number(row, 17, entry.offset_before[2] as f64, None)?;
        worksheet.write_number(row, 18, entry.offset_after[2] as f64, None)?;
        worksheet.write_number(row, 19, entry.position_over[2] as f64, None)?;
        worksheet.write_number(row, 20, entry.position_under[2] as f64, None)?;
        worksheet.write_number(row, 21, entry.peak[2] as f64, None)?;
        worksheet.write_number(row, 22, entry.peak_position[2] as f64, None)?;

        worksheet.write_number(row, 23, entry.offset_before[3] as f64, None)?;
        worksheet.write_number(row, 24, entry.offset_after[3] as f64, None)?;
        worksheet.write_number(row, 25, entry.position_over[3] as f64, None)?;
        worksheet.write_number(row, 26, entry.position_under[3] as f64, None)?;
        worksheet.write_number(row, 27, entry.peak[3] as f64, None)?;
        worksheet.write_number(row, 28, entry.peak_position[3] as f64, None)?;

        worksheet.write_number(row, 29, entry.offset_before[4] as f64, None)?;
        worksheet.write_number(row, 30, entry.offset_after[4] as f64, None)?;
        worksheet.write_number(row, 31, entry.position_over[4] as f64, None)?;
        worksheet.write_number(row, 32, entry.position_under[4] as f64, None)?;
        worksheet.write_number(row, 33, entry.peak[4] as f64, None)?;
        worksheet.write_number(row, 34, entry.peak_position[4] as f64, None)?;

        worksheet.write_number(row, 35, entry.offset_before[5] as f64, None)?;
        worksheet.write_number(row, 36, entry.offset_after[5] as f64, None)?;
        worksheet.write_number(row, 37, entry.position_over[5] as f64, None)?;
        worksheet.write_number(row, 38, entry.position_under[5] as f64, None)?;
        worksheet.write_number(row, 39, entry.peak[5] as f64, None)?;
        worksheet.write_number(row, 40, entry.peak_position[5] as f64, None)?;

        worksheet.write_number(row, 41, entry.offset_before[6] as f64, None)?;
        worksheet.write_number(row, 42, entry.offset_after[6] as f64, None)?;
        worksheet.write_number(row, 43, entry.position_over[6] as f64, None)?;
        worksheet.write_number(row, 44, entry.position_under[6] as f64, None)?;
        worksheet.write_number(row, 45, entry.peak[6] as f64, None)?;
        worksheet.write_number(row, 46, entry.peak_position[6] as f64, None)?;
        
        worksheet.write_number(row, 47, entry.offset_before[7] as f64, None)?;
        worksheet.write_number(row, 48, entry.offset_after[7] as f64, None)?;
        worksheet.write_number(row, 49, entry.position_over[7] as f64, None)?;
        worksheet.write_number(row, 50, entry.position_under[7] as f64, None)?;
        worksheet.write_number(row, 51, entry.peak[7] as f64, None)?;
        worksheet.write_number(row, 52, entry.peak_position[7] as f64, None)?;

        worksheet.write_number(row, 53, entry.offset_before[8] as f64, None)?;
        worksheet.write_number(row, 54, entry.offset_after[8] as f64, None)?;
        worksheet.write_number(row, 55, entry.position_over[8] as f64, None)?;
        worksheet.write_number(row, 56, entry.position_under[8] as f64, None)?;
        worksheet.write_number(row, 57, entry.peak[8] as f64, None)?;
        worksheet.write_number(row, 58, entry.peak_position[8] as f64, None)?;

        worksheet.write_number(row, 59, entry.offset_before[9] as f64, None)?;
        worksheet.write_number(row, 60, entry.offset_after[9] as f64, None)?;
        worksheet.write_number(row, 61, entry.position_over[9] as f64, None)?;
        worksheet.write_number(row, 62, entry.position_under[9] as f64, None)?;
        worksheet.write_number(row, 63, entry.peak[9] as f64, None)?;
        worksheet.write_number(row, 64, entry.peak_position[9] as f64, None)?;

        worksheet.write_number(row, 65, entry.offset_before[10] as f64, None)?;
        worksheet.write_number(row, 66, entry.offset_after[10] as f64, None)?;
        worksheet.write_number(row, 67, entry.position_over[10] as f64, None)?;
        worksheet.write_number(row, 68, entry.position_under[10] as f64, None)?;
        worksheet.write_number(row, 69, entry.peak[10] as f64, None)?;
        worksheet.write_number(row, 70, entry.peak_position[10] as f64, None)?;
        
    }
    Ok(())
}


pub async fn store_additional_info_data_as_xlsx_12CH(data: &Vec<UdpTag49>,name: &str, ip: &str) -> Result<(), Box<dyn Error>> {
    // Create the workbook and worksheet
    let workbook = Workbook::new(name)?;
    let mut worksheet = workbook.add_worksheet(None)?;

    // Write headers
    let headers = ["Zeitstempel Erstellt", "Sensor IP", "Fortlaufender Zähler", "Zeitstempel Messung", "Highphase Messtrigger",
     "Offset Start CH0", "Offset Ende CH0", "Kurve Start CH0", "Kurve Ende CH0", "Peakwert CH0", "Peakposition CH0",
     "Offset Start CH1", "Offset Ende CH1", "Kurve Start CH1", "Kurve Ende CH1", "Peakwert CH1", "Peakposition CH1",
     "Offset Start CH2", "Offset Ende CH2", "Kurve Start CH2", "Kurve Ende CH2", "Peakwert CH2", "Peakposition CH2",
     "Offset Start CH3", "Offset Ende CH3", "Kurve Start CH3", "Kurve Ende CH3", "Peakwert CH3", "Peakposition CH3",
     "Offset Start CH4", "Offset Ende CH4", "Kurve Start CH4", "Kurve Ende CH4", "Peakwert CH4", "Peakposition CH4",
     "Offset Start CH5", "Offset Ende CH5", "Kurve Start CH5", "Kurve Ende CH5", "Peakwert CH5", "Peakposition CH5",
     "Offset Start CH6", "Offset Ende CH6", "Kurve Start CH6", "Kurve Ende CH6", "Peakwert CH6", "Peakposition CH6",
     "Offset Start CH7", "Offset Ende CH7", "Kurve Start CH7", "Kurve Ende CH7", "Peakwert CH7", "Peakposition CH7",
    "Offset Start CH8", "Offset Ende CH8", "Kurve Start CH8", "Kurve Ende CH8", "Peakwert CH8", "Peakposition CH8",
    "Offset Start CH9", "Offset Ende CH9", "Kurve Start CH9", "Kurve Ende CH9", "Peakwert CH9", "Peakposition CH9",
    "Offset Start CH10", "Offset Ende CH10", "Kurve Start CH10", "Kurve Ende CH10", "Peakwert CH10", "Peakposition CH10",
    "Offset Start CH11", "Offset Ende CH11", "Kurve Start CH11", "Kurve Ende CH11", "Peakwert CH11", "Peakposition CH11",
    ];
    for (col, header) in headers.iter().enumerate() {
        worksheet.write_string(0, col as u16, header, None)?;
    }
    for (i, entry) in data.iter().enumerate() {
        let row = (i + 1) as u32; // Start at the second row
        
        worksheet.write_string(row, 0, &entry.created, None)?;
        worksheet.write_string(row, 1, ip, None)?;
        worksheet.write_number(row, 2, entry.counter as f64, None)?;
        worksheet.write_string(row, 3, &entry.timestamp, None)?;
        worksheet.write_number(row, 4, entry.len_trigger as f64, None)?;

        worksheet.write_number(row, 5, entry.offset_before[0] as f64, None)?;
        worksheet.write_number(row, 6, entry.offset_after[0] as f64, None)?;
        worksheet.write_number(row, 7, entry.position_over[0] as f64, None)?;
        worksheet.write_number(row, 8, entry.position_under[0] as f64, None)?;
        worksheet.write_number(row, 9, entry.peak[0] as f64, None)?;
        worksheet.write_number(row, 10, entry.peak_position[0] as f64, None)?;

        worksheet.write_number(row, 11, entry.offset_before[1] as f64, None)?;
        worksheet.write_number(row, 12, entry.offset_after[1] as f64, None)?;
        worksheet.write_number(row, 13, entry.position_over[1] as f64, None)?;
        worksheet.write_number(row, 14, entry.position_under[1] as f64, None)?;
        worksheet.write_number(row, 15, entry.peak[1] as f64, None)?;
        worksheet.write_number(row, 16, entry.peak_position[1] as f64, None)?;


        worksheet.write_number(row, 17, entry.offset_before[2] as f64, None)?;
        worksheet.write_number(row, 18, entry.offset_after[2] as f64, None)?;
        worksheet.write_number(row, 19, entry.position_over[2] as f64, None)?;
        worksheet.write_number(row, 20, entry.position_under[2] as f64, None)?;
        worksheet.write_number(row, 21, entry.peak[2] as f64, None)?;
        worksheet.write_number(row, 22, entry.peak_position[2] as f64, None)?;

        worksheet.write_number(row, 23, entry.offset_before[3] as f64, None)?;
        worksheet.write_number(row, 24, entry.offset_after[3] as f64, None)?;
        worksheet.write_number(row, 25, entry.position_over[3] as f64, None)?;
        worksheet.write_number(row, 26, entry.position_under[3] as f64, None)?;
        worksheet.write_number(row, 27, entry.peak[3] as f64, None)?;
        worksheet.write_number(row, 28, entry.peak_position[3] as f64, None)?;

        worksheet.write_number(row, 29, entry.offset_before[4] as f64, None)?;
        worksheet.write_number(row, 30, entry.offset_after[4] as f64, None)?;
        worksheet.write_number(row, 31, entry.position_over[4] as f64, None)?;
        worksheet.write_number(row, 32, entry.position_under[4] as f64, None)?;
        worksheet.write_number(row, 33, entry.peak[4] as f64, None)?;
        worksheet.write_number(row, 34, entry.peak_position[4] as f64, None)?;

        worksheet.write_number(row, 35, entry.offset_before[5] as f64, None)?;
        worksheet.write_number(row, 36, entry.offset_after[5] as f64, None)?;
        worksheet.write_number(row, 37, entry.position_over[5] as f64, None)?;
        worksheet.write_number(row, 38, entry.position_under[5] as f64, None)?;
        worksheet.write_number(row, 39, entry.peak[5] as f64, None)?;
        worksheet.write_number(row, 40, entry.peak_position[5] as f64, None)?;

        worksheet.write_number(row, 41, entry.offset_before[6] as f64, None)?;
        worksheet.write_number(row, 42, entry.offset_after[6] as f64, None)?;
        worksheet.write_number(row, 43, entry.position_over[6] as f64, None)?;
        worksheet.write_number(row, 44, entry.position_under[6] as f64, None)?;
        worksheet.write_number(row, 45, entry.peak[6] as f64, None)?;
        worksheet.write_number(row, 46, entry.peak_position[6] as f64, None)?;
        
        worksheet.write_number(row, 47, entry.offset_before[7] as f64, None)?;
        worksheet.write_number(row, 48, entry.offset_after[7] as f64, None)?;
        worksheet.write_number(row, 49, entry.position_over[7] as f64, None)?;
        worksheet.write_number(row, 50, entry.position_under[7] as f64, None)?;
        worksheet.write_number(row, 51, entry.peak[7] as f64, None)?;
        worksheet.write_number(row, 52, entry.peak_position[7] as f64, None)?;

        worksheet.write_number(row, 53, entry.offset_before[8] as f64, None)?;
        worksheet.write_number(row, 54, entry.offset_after[8] as f64, None)?;
        worksheet.write_number(row, 55, entry.position_over[8] as f64, None)?;
        worksheet.write_number(row, 56, entry.position_under[8] as f64, None)?;
        worksheet.write_number(row, 57, entry.peak[8] as f64, None)?;
        worksheet.write_number(row, 58, entry.peak_position[8] as f64, None)?;

        worksheet.write_number(row, 59, entry.offset_before[9] as f64, None)?;
        worksheet.write_number(row, 60, entry.offset_after[9] as f64, None)?;
        worksheet.write_number(row, 61, entry.position_over[9] as f64, None)?;
        worksheet.write_number(row, 62, entry.position_under[9] as f64, None)?;
        worksheet.write_number(row, 63, entry.peak[9] as f64, None)?;
        worksheet.write_number(row, 64, entry.peak_position[9] as f64, None)?;

        worksheet.write_number(row, 65, entry.offset_before[10] as f64, None)?;
        worksheet.write_number(row, 66, entry.offset_after[10] as f64, None)?;
        worksheet.write_number(row, 67, entry.position_over[10] as f64, None)?;
        worksheet.write_number(row, 68, entry.position_under[10] as f64, None)?;
        worksheet.write_number(row, 69, entry.peak[10] as f64, None)?;
        worksheet.write_number(row, 70, entry.peak_position[10] as f64, None)?;

        worksheet.write_number(row, 71, entry.offset_before[11] as f64, None)?;
        worksheet.write_number(row, 72, entry.offset_after[11] as f64, None)?;
        worksheet.write_number(row, 73, entry.position_over[11] as f64, None)?;
        worksheet.write_number(row, 74, entry.position_under[11] as f64, None)?;
        worksheet.write_number(row, 75, entry.peak[11] as f64, None)?;
        worksheet.write_number(row, 76, entry.peak_position[11] as f64, None)?;

    }
    Ok(())
}



async fn process_additonal_info_data(result: Response, ip_address: &str, name: &str, select_type: u8, number_of_channels:u8) -> Result<Vec<(u64, u16, u8, u16, u16, u16, u16, u16, u16, String)>, Box<dyn Error>> {
    let mut data = result;
    let data: Vec<UdpTag49> = match data.take(0) {
        Ok(data) => data,
        Err(e) => {
            println!("Error selecting additional info data: {:?}", e);
            return Err(Box::new(e));
        }
    };
    // let number_of_channels = match get_number_of_channels_tag49(&data).await {
    //     Ok(number_of_channels) => number_of_channels,
    //     Err(e) => {
    //         println!("Error getting number of channels: {:?}", e);
    //         0
    //     }
    // };
    let ip = ip_address;
    

    match number_of_channels {
        1 => {
            store_additional_info_data_as_xlsx_1CH(&data, name, ip).await?;
        }
        2 => {
            store_additional_info_data_as_xlsx_2CH(&data, name, ip).await?;
        }
        3 => {
            store_additional_info_data_as_xlsx_3CH(&data, name, ip).await?;
        }
        4 => {
            store_additional_info_data_as_xlsx_4CH(&data, name, ip).await?;
        }
        5 => {
            store_additional_info_data_as_xlsx_5CH(&data, name, ip).await?;
        }
        6 => {
            store_additional_info_data_as_xlsx_6CH(&data, name, ip).await?;
        }
        7 => {
            store_additional_info_data_as_xlsx_7CH(&data, name, ip).await?;
        }
        8 => {
            store_additional_info_data_as_xlsx_8CH(&data, name, ip).await?;
        }
        9 => {
            store_additional_info_data_as_xlsx_9CH(&data, name, ip).await?;
        }
        10 => {
            store_additional_info_data_as_xlsx_10CH(&data, name, ip).await?;
        }
        11 => {
            store_additional_info_data_as_xlsx_11CH(&data, name, ip).await?;
        }
        _ => {
            println!("Number of channels not supported");
        }
    };
    if select_type == 1 {
        return Ok(Vec::new());
    }

    let exploded_data: Vec<(u64, u16, u8, u16, u16, u16, u16, u16, u16, String)> = data
        .into_iter()
        .flat_map(|tag| {
            tag.channel.into_iter()
                .zip(tag.peak.into_iter()) // Combine the channel and peak vectors
                .zip(tag.peak_position.into_iter())
                .zip(tag.position_over.into_iter())
                .zip(tag.position_under.into_iter())
                .zip(tag.offset_after.into_iter())
                .zip(tag.offset_before.into_iter())
                .map(move |((((((channel_value, peak_value), peak_position), position_over), position_under), offset_after), offset_before)| {
                    (tag.run_counter, tag.len_trigger, channel_value, peak_value, peak_position, position_over, position_under, offset_after, offset_before, tag.timestamp.clone())
                })
        })
        .collect();
    Ok(exploded_data)
}

// Main function that uses both helper functions
async fn select_additional_info_data_async(
    ip: &str,
    port: &str,
    user: &str,
    pw: &str,
    namespace: &str,
    db_name: &str,
    table_name: &str,
    run_id: &str,
    path_name: &str,
    select_type: u8
) -> Result<Vec<(u64, u16, u8, u16, u16, u16, u16, u16, u16, String)>, Box<dyn Error>> {
    let db = connect_to_db(ip, port, user, pw, namespace, db_name).await?;

    // let mut general_info_result = query_general_information(&db, "amv_tag_40", run_id).await?;
    let mut general_info_result = query_amv_static_info(&db, "amv_static_info", run_id).await?;
    let general_info : Vec<AmvStaticInfo> = match general_info_result.take(0) {
        Ok(data) => data,
        Err(e) => {
            println!("Error selecting measurement data: {:?}", e);
            return Err(Box::new(e));
        }
    };
    let ip = format!("{}.{}.{}.{}", general_info[0].ip_address[0], general_info[0].ip_address[1], general_info[0].ip_address[2], general_info[0].ip_address[3]);

    let number_of_channels = general_info[0].number_of_channels;
    let result = query_additonal_info_data(&db, table_name, run_id).await?;
    let data = process_additonal_info_data(result, &ip,path_name, select_type, number_of_channels).await?;
    Ok(data)
}

// Main function that uses both helper functions
async fn select_measurement_data_async(
    ip: &str,
    port: &str,
    user: &str,
    pw: &str,
    namespace: &str,
    db_name: &str,
    table_name: &str,
    run_id: &str,
    path_name: &str, 
    select_type: u8
) -> Result<Vec<(u64, u8, u64, u64, u16, u16, u16, u16, u16, String, String, Vec<String>)>, Box<dyn Error>> {
    let db = connect_to_db(ip, port, user, pw, namespace, db_name).await?;
    
    let mut general_info_result = query_amv_static_info(&db, "amv_static_info", run_id).await?;
    let general_info : Vec<AmvStaticInfo> = match general_info_result.take(0) {
        Ok(data) => data,
        Err(e) => {
            println!("Error selecting general_info: {:?}", e);
            return Err(Box::new(e));
        }
    };
    let ip = format!("{}.{}.{}.{}", general_info[0].ip_address[0], general_info[0].ip_address[1], general_info[0].ip_address[2], general_info[0].ip_address[3]);
    let number_of_channels = general_info[0].number_of_channels;
    let result = query_measurement_data(&db, table_name, run_id).await?;
    let data = process_measurement_data(result, &ip, path_name, select_type, number_of_channels).await?;
    Ok(data)
}

pub async fn get_number_of_channels_tag41(data: &Vec<UdpTag41>) -> Result<u8, Box<dyn Error>> {
    let number_of_channels = data[0].channel.len() as u8;
    Ok(number_of_channels)
}

pub async fn get_number_of_channels_tag49(data: &Vec<UdpTag49>) -> Result<u8, Box<dyn Error>> {
    let number_of_channels = data[0].channel.len() as u8;
    Ok(number_of_channels)
}

pub async fn error_matching(vec: &Vec<String>) -> Result<Vec<String>, Box<dyn Error>> {
    let mut status = vec.clone();
    for i in 0..status.len() {
        if status[i] == "00" {
            status[i] = "OK: Messwert im Toleranzbereich".to_string();
        } else if status[i] == "01" {
            "OK: Der Massewert überschreitet den Toleranzbereich".to_string();
        } else if status[i] == "02" {
            "OK: Der Massewert unterschreitet den Toleranzbereich".to_string();
        } else if status[i] == "03" {
            "FEHLER: Offsetabgleich Anschlag Stellgröße oben".to_string();
        } else if status[i] == "04" {
            "FEHLER: Offsetabgleich Anschlag Stellgröße unten".to_string();
        } else if status[i] == "05" {
            "FEHLER: Offsetabgleich war noch nicht fertig, als die Flanke des Offsettriggers kam".to_string();
        } else if status[i] == "06" {
            "FEHLER: Seit dem letzten Systemstart ist keine Messung vorhanden".to_string();
        } else if status[i] == "07" {
            "FEHLER: Der Offset befindet sich außerhalb des Messbereichs".to_string();
        } else if status[i] == "08" {
            "FEHLER: Der Messtrigger ist zu lang".to_string();
        } else if status[i] == "09" {
            "FEHLER: Der Messtrigger ist zu kurz".to_string();
        } else if status[i] == "10" {
            "FEHLER: Schräge Nulllinie: Schwellwert2 wurde nicht unterschritten".to_string();
        } else if status[i] == "11" {
            "FEHLER: Schräge Nulllinie: Zeit t1 liegt vor der steigenden Flanke des Messtriggers".to_string();
        } else if status[i] == "12" {
            "FEHLER: Schräge Nulllinie: Zeit t2 liegt nach der fallenden Flanke des Messtriggers".to_string();
        } else if status[i] == "13" {
            "FEHLER: Nulllinien Mittelung".to_string();
        } else if status[i] == "14" {
            "FEHLER: Nulllinien Berechnung".to_string();
        } else if status[i] == "15" {
            "FEHLER: maximal zulässige Anzahl von Umkehrpunkten wurde überschritten".to_string();
        } else if status[i] == "16" {
            "FEHLER: maximal zulässige Amplitude des Rauschens wurde überschritten".to_string();
        } else if status[i] == "17" {
            "FEHLER: Ein unzulässig hoher negativer Peak war vorhanden".to_string();
        } else if status[i] == "0A" {
            "FEHLER: Anschlag des Messsignals".to_string();
        } else if status[i] == "0B" {
            "FEHLER: Ein Variablenüberlauf bei der Masseberechnung ist aufgetreten".to_string();
        } else if status[i] == "0C" {
            "FEHLER: Überwachung des Messfensters - positiv".to_string();
        } else if status[i] == "0D" {
            "FEHLER: Überwachung des Messfensters - negativ".to_string();
        } else if status[i] == "0E" {
            "FEHLER: Bei dem Offsetabgleich ist ein Timeout aufgetreten".to_string();
        } else if status[i] == "0F" {
            "FEHLER: Schräge Nulllinie: Schwellwert1 wurde nicht überschritten".to_string();
        }
    }
    Ok(status)
}

pub async fn query_measurement_data(
    db: &Surreal<Client>,
    table_name: &str,
    run_id: &str
) -> Result<surrealdb::Response, Box<dyn Error>>{
    let result_query = format!(
        "SELECT run_counter,channel, integral, mass, offset, offset1, offset2, tolerance_bottom, tolerance_top, project, timestamp, status, counter, created  FROM {} WHERE run_id = {} ORDER BY run_counter ASC",
        table_name, run_id
    );
    let result = db.query(&result_query).await?;
    Ok(result)
}

pub async fn store_measurement_data_as_xlsx_1CH(data: &Vec<UdpTag41>,name: &str, ip: &str) -> Result<(), Box<dyn Error>> {
    // Create the workbook and worksheet
    let workbook = Workbook::new(name)?;
    let mut worksheet = workbook.add_worksheet(None)?;

    // Write headers
    let headers = ["Zeitstempel Erstellt", "Sensor IP", "Fortlaufender Zähler", "Zeitstempel des letzten Offsetabgleichs", "Dauer des letzten Offsetabgleichs", "Zeitstempel Messung",
     "Integral_CH0", "Masse_CHO", "Offsetwert_CH0", "Offsetwert1_CH0", "Offsetwert2_CH0", "Grenze_Masse_unten_CH0", "Grenze_Masse_oben_CH0", "Status_der_Messung_CH0",
    ];
    for (col, header) in headers.iter().enumerate() {
        worksheet.write_string(0, col as u16, header, None)?;
    }
    for (i, entry) in data.iter().enumerate() {
        let row = (i + 1) as u32; // Start at the second row
        
        worksheet.write_string(row, 0, &entry.created, None)?;
        worksheet.write_string(row, 1, ip, None)?;
        worksheet.write_number(row, 2, entry.counter as f64, None)?;
        worksheet.write_string(row, 5, &entry.timestamp, None)?;

        worksheet.write_number(row, 6, entry.integral[0] as f64, None)?;
        worksheet.write_number(row, 7, entry.mass[0] as f64, None)?;
        worksheet.write_number(row, 8, entry.offset[0] as f64, None)?;
        worksheet.write_number(row, 9, entry.offset1[0] as f64, None)?;
        worksheet.write_number(row, 10, entry.offset2[0] as f64, None)?;
        worksheet.write_number(row, 11, entry.tolerance_bottom[0] as f64, None)?;
        worksheet.write_number(row, 12, entry.tolerance_top[0] as f64, None)?;
        let status = error_matching(&entry.status[0]).await?;
        worksheet.write_string(row, 13, &status.join(","), None)?;
    }
    Ok(())
}

pub async fn store_measurement_data_as_xlsx_2CH(data: &Vec<UdpTag41>,name: &str, ip: &str) -> Result<(), Box<dyn Error>> {
    // Create the workbook and worksheet
    let workbook = Workbook::new(name)?;
    let mut worksheet = workbook.add_worksheet(None)?;

    //let ip = "172.30.1.122";

    // Write headers
    let headers = ["Zeitstempel Erstellt", "Sensor IP", "Fortlaufender Zähler", "Zeitstempel des letzten Offsetabgleichs", "Dauer des letzten Offsetabgleichs", "Zeitstempel Messung",
     "Integral_CH0", "Masse_CHO", "Offsetwert_CH0", "Offsetwert1_CH0", "Offsetwert2_CH0", "Grenze_Masse_unten_CH0", "Grenze_Masse_oben_CH0", "Status_der_Messung_CH0",
     "Integral_CH1", "Masse_CH1", "Offsetwert_CH1", "Offsetwert1_CH1", "Offsetwert2_CH1", "Grenze_Masse_unten_CH1", "Grenze_Masse_oben_CH1", "Status_der_Messung_CH1"];
    for (col, header) in headers.iter().enumerate() {
        worksheet.write_string(0, col as u16, header, None)?;
    }
    for (i, entry) in data.iter().enumerate() {
        let row = (i + 1) as u32; // Start at the second row
        
        worksheet.write_string(row, 0, &entry.created, None)?;
        worksheet.write_string(row, 1, ip, None)?;
        worksheet.write_number(row, 2, entry.counter as f64, None)?;
        worksheet.write_string(row, 5, &entry.timestamp, None)?;

        worksheet.write_number(row, 6, entry.integral[0] as f64, None)?;
        worksheet.write_number(row, 7, entry.mass[0] as f64, None)?;
        worksheet.write_number(row, 8, entry.offset[0] as f64, None)?;
        worksheet.write_number(row, 9, entry.offset1[0] as f64, None)?;
        worksheet.write_number(row, 10, entry.offset2[0] as f64, None)?;
        worksheet.write_number(row, 11, entry.tolerance_bottom[0] as f64, None)?;
        worksheet.write_number(row, 12, entry.tolerance_top[0] as f64, None)?;
        let status = error_matching(&entry.status[0]).await?;
        worksheet.write_string(row, 13, &status.join(","), None)?;


        worksheet.write_number(row, 14, entry.integral[1] as f64, None)?;
        worksheet.write_number(row, 15, entry.mass[1] as f64, None)?;
        worksheet.write_number(row, 16, entry.offset[1] as f64, None)?;
        worksheet.write_number(row, 17, entry.offset1[1] as f64, None)?;
        worksheet.write_number(row, 18, entry.offset2[1] as f64, None)?;
        worksheet.write_number(row, 19, entry.tolerance_bottom[1] as f64, None)?;
        worksheet.write_number(row, 20, entry.tolerance_top[1] as f64, None)?;
        let status = error_matching(&entry.status[1]).await?;
        worksheet.write_string(row, 21, &status.join(","), None)?;
    }
    Ok(())
}

pub async fn store_measurement_data_as_xlsx_3CH(data: &Vec<UdpTag41>,name: &str, ip: &str) -> Result<(), Box<dyn Error>> {
    // Create the workbook and worksheet
    let workbook = Workbook::new(name)?;
    let mut worksheet = workbook.add_worksheet(None)?;

    //let ip = "172.30.1.122";
    let headers = ["Zeitstempel Erstellt", "Sensor IP", "Fortlaufender Zähler", "Zeitstempel des letzten Offsetabgleichs", "Dauer des letzten Offsetabgleichs", "Zeitstempel Messung",
     "Integral_CH0", "Masse_CHO", "Offsetwert_CH0", "Offsetwert1_CH0", "Offsetwert2_CH0", "Grenze_Masse_unten_CH0", "Grenze_Masse_oben_CH0", "Status_der_Messung_CH0",
     "Integral_CH1", "Masse_CH1", "Offsetwert_CH1", "Offsetwert1_CH1", "Offsetwert2_CH1", "Grenze_Masse_unten_CH1", "Grenze_Masse_oben_CH1", "Status_der_Messung_CH1",
     "Integral_CH2", "Masse_CH2", "Offsetwert_CH2", "Offsetwert1_CH2", "Offsetwert2_CH2", "Grenze_Masse_unten_CH2", "Grenze_Masse_oben_CH2", "Status_der_Messung_CH2"];

    for (col, header) in headers.iter().enumerate() {
        worksheet.write_string(0, col as u16, header, None)?;
    }

    for (i, entry) in data.iter().enumerate() {
        let row = (i + 1) as u32; // Start at the second row
        
        worksheet.write_string(row, 0, &entry.created, None)?;
        worksheet.write_string(row, 1, ip, None)?;
        worksheet.write_number(row, 2, entry.counter as f64, None)?;
        worksheet.write_string(row, 5, &entry.timestamp, None)?;

        worksheet.write_number(row, 6, entry.integral[0] as f64, None)?;
        worksheet.write_number(row, 7, entry.mass[0] as f64, None)?;
        worksheet.write_number(row, 8, entry.offset[0] as f64, None)?;
        worksheet.write_number(row, 9, entry.offset1[0] as f64, None)?;
        worksheet.write_number(row, 10, entry.offset2[0] as f64, None)?;
        worksheet.write_number(row, 11, entry.tolerance_bottom[0] as f64, None)?;
        worksheet.write_number(row, 12, entry.tolerance_top[0] as f64, None)?;
        let status = error_matching(&entry.status[0]).await?;
        worksheet.write_string(row, 13, &status.join(","), None)?;

        worksheet.write_number(row, 14, entry.integral[1] as f64, None)?;
        worksheet.write_number(row, 15, entry.mass[1] as f64, None)?;
        worksheet.write_number(row, 16, entry.offset[1] as f64, None)?;
        worksheet.write_number(row, 17, entry.offset1[1] as f64, None)?;
        worksheet.write_number(row, 18, entry.offset2[1] as f64, None)?;
        worksheet.write_number(row, 19, entry.tolerance_bottom[1] as f64, None)?;
        worksheet.write_number(row, 20, entry.tolerance_top[1] as f64, None)?;
        let status = error_matching(&entry.status[1]).await?;
        worksheet.write_string(row, 21, &status.join(","), None)?;

        worksheet.write_number(row, 22, entry.integral[2] as f64, None)?;
        worksheet.write_number(row, 23, entry.mass[2] as f64, None)?;
        worksheet.write_number(row, 24, entry.offset[2] as f64, None)?;
        worksheet.write_number(row, 25, entry.offset1[2] as f64, None)?;
        worksheet.write_number(row, 26, entry.offset2[2] as f64, None)?;
        worksheet.write_number(row, 27, entry.tolerance_bottom[2] as f64, None)?;
        worksheet.write_number(row, 28, entry.tolerance_top[2] as f64, None)?;
        let status = error_matching(&entry.status[2]).await?;
        worksheet.write_string(row, 29, &status.join(","), None)?;

    }
    Ok(())
}

pub async fn store_measurement_data_as_xlsx_4CH(data: &Vec<UdpTag41>,name: &str, ip: &str) -> Result<(), Box<dyn Error>> {
    // Create the workbook and worksheet
    let workbook = Workbook::new(name)?;
    let mut worksheet = workbook.add_worksheet(None)?;

    //let ip = "172.30.1.122";

    // Write headers
    let headers = ["Zeitstempel Erstellt", "Sensor IP", "Fortlaufender Zähler", "Zeitstempel des letzten Offsetabgleichs", "Dauer des letzten Offsetabgleichs", "Zeitstempel Messung",
     "Integral_CH0", "Masse_CHO", "Offsetwert_CH0", "Offsetwert1_CH0", "Offsetwert2_CH0", "Grenze_Masse_unten_CH0", "Grenze_Masse_oben_CH0", "Status_der_Messung_CH0",
     "Integral_CH1", "Masse_CH1", "Offsetwert_CH1", "Offsetwert1_CH1", "Offsetwert2_CH1", "Grenze_Masse_unten_CH1", "Grenze_Masse_oben_CH1", "Status_der_Messung_CH1",
     "Integral_CH2", "Masse_CH2", "Offsetwert_CH2", "Offsetwert1_CH2", "Offsetwert2_CH2", "Grenze_Masse_unten_CH2", "Grenze_Masse_oben_CH2", "Status_der_Messung_CH2",
     "Integral_CH3", "Masse_CH3", "Offsetwert_CH3", "Offsetwert1_CH3", "Offsetwert2_CH3", "Grenze_Masse_unten_CH3", "Grenze_Masse_oben_CH3", "Status_der_Messung_CH3"];

    for (col, header) in headers.iter().enumerate() {
        worksheet.write_string(0, col as u16, header, None)?;

    }

    for (i, entry) in data.iter().enumerate() {
        let row = (i + 1) as u32; // Start at the second row
        
        worksheet.write_string(row, 0, &entry.created, None)?;
        worksheet.write_string(row, 1, ip, None)?;
        worksheet.write_number(row, 2, entry.counter as f64, None)?;
        worksheet.write_string(row, 5, &entry.timestamp, None)?;

        worksheet.write_number(row, 6, entry.integral[0] as f64, None)?;
        worksheet.write_number(row, 7, entry.mass[0] as f64, None)?;
        worksheet.write_number(row, 8, entry.offset[0] as f64, None)?;
        worksheet.write_number(row, 9, entry.offset1[0] as f64, None)?;
        worksheet.write_number(row, 10, entry.offset2[0] as f64, None)?;
        worksheet.write_number(row, 11, entry.tolerance_bottom[0] as f64, None)?;
        worksheet.write_number(row, 12, entry.tolerance_top[0] as f64, None)?;
        let status = error_matching(&entry.status[0]).await?;
        worksheet.write_string(row, 13, &status.join(","), None)?;

        worksheet.write_number(row, 14, entry.integral[1] as f64, None)?;
        worksheet.write_number(row, 15, entry.mass[1] as f64, None)?;
        worksheet.write_number(row, 16, entry.offset[1] as f64, None)?;
        worksheet.write_number(row, 17, entry.offset1[1] as f64, None)?;
        worksheet.write_number(row, 18, entry.offset2[1] as f64, None)?;
        worksheet.write_number(row, 19, entry.tolerance_bottom[1] as f64, None)?;
        worksheet.write_number(row, 20, entry.tolerance_top[1] as f64, None)?;
        let status = error_matching(&entry.status[1]).await?;
        worksheet.write_string(row, 21, &status.join(","), None)?;

        worksheet.write_number(row, 22, entry.integral[2] as f64, None)?;
        worksheet.write_number(row, 23, entry.mass[2] as f64, None)?;
        worksheet.write_number(row, 24, entry.offset[2] as f64, None)?;
        worksheet.write_number(row, 25, entry.offset1[2] as f64, None)?;
        worksheet.write_number(row, 26, entry.offset2[2] as f64, None)?;
        worksheet.write_number(row, 27, entry.tolerance_bottom[2] as f64, None)?;
        worksheet.write_number(row, 28, entry.tolerance_top[2] as f64, None)?;
        let status = error_matching(&entry.status[2]).await?;
        worksheet.write_string(row, 29, &status.join(","), None)?;

        worksheet.write_number(row, 30, entry.integral[3] as f64, None)?;
        worksheet.write_number(row, 31, entry.mass[3] as f64, None)?;
        worksheet.write_number(row, 32, entry.offset[3] as f64, None)?;
        worksheet.write_number(row, 33, entry.offset1[3] as f64, None)?;
        worksheet.write_number(row, 34, entry.offset2[3] as f64, None)?;
        worksheet.write_number(row, 35, entry.tolerance_bottom[3] as f64, None)?;
        worksheet.write_number(row, 36, entry.tolerance_top[3] as f64, None)?;
        let status = error_matching(&entry.status[3]).await?;
        worksheet.write_string(row, 37, &status.join(","), None)?;
    }

    Ok(())
}


pub async fn store_measurement_data_as_xlsx_5CH(data: &Vec<UdpTag41>, name: &str, ip: &str) -> Result<(), Box<dyn Error>> {
    // Create the workbook and worksheet
    let workbook = Workbook::new(name)?;
    let mut worksheet = workbook.add_worksheet(None)?;

    // Write headers
    let headers = ["Zeitstempel Erstellt", "Sensor IP", "Fortlaufender Zähler", "Zeitstempel des letzten Offsetabgleichs", "Dauer des letzten Offsetabgleichs", "Zeitstempel Messung",
     "Integral_CH0", "Masse_CHO", "Offsetwert_CH0", "Offsetwert1_CH0", "Offsetwert2_CH0", "Grenze_Masse_unten_CH0", "Grenze_Masse_oben_CH0", "Status_der_Messung_CH0",
     "Integral_CH1", "Masse_CH1", "Offsetwert_CH1", "Offsetwert1_CH1", "Offsetwert2_CH1", "Grenze_Masse_unten_CH1", "Grenze_Masse_oben_CH1", "Status_der_Messung_CH1",
     "Integral_CH2", "Masse_CH2", "Offsetwert_CH2", "Offsetwert1_CH2", "Offsetwert2_CH2", "Grenze_Masse_unten_CH2", "Grenze_Masse_oben_CH2", "Status_der_Messung_CH2",
     "Integral_CH3", "Masse_CH3", "Offsetwert_CH3", "Offsetwert1_CH3", "Offsetwert2_CH3", "Grenze_Masse_unten_CH3", "Grenze_Masse_oben_CH3", "Status_der_Messung_CH3",
     "Integral_CH4", "Masse_CH4", "Offsetwert_CH4", "Offsetwert1_CH4", "Offsetwert2_CH4", "Grenze_Masse_unten_CH4", "Grenze_Masse_oben_CH4", "Status_der_Messung_CH4"];

    for (col, header) in headers.iter().enumerate() {
        worksheet.write_string(0, col as u16, header, None)?;

    }

    for (i, entry) in data.iter().enumerate() {
        let row = (i + 1) as u32; // Start at the second row
        
        worksheet.write_string(row, 0, &entry.created, None)?;
        worksheet.write_string(row, 1, ip, None)?;
        worksheet.write_number(row, 2, entry.counter as f64, None)?;
        worksheet.write_string(row, 5, &entry.timestamp, None)?;

        worksheet.write_number(row, 6, entry.integral[0] as f64, None)?;
        worksheet.write_number(row, 7, entry.mass[0] as f64, None)?;
        worksheet.write_number(row, 8, entry.offset[0] as f64, None)?;
        worksheet.write_number(row, 9, entry.offset1[0] as f64, None)?;
        worksheet.write_number(row, 10, entry.offset2[0] as f64, None)?;
        worksheet.write_number(row, 11, entry.tolerance_bottom[0] as f64, None)?;
        worksheet.write_number(row, 12, entry.tolerance_top[0] as f64, None)?;
        let status = error_matching(&entry.status[0]).await?;
        worksheet.write_string(row, 13, &status.join(","), None)?;

        worksheet.write_number(row, 14, entry.integral[1] as f64, None)?;
        worksheet.write_number(row, 15, entry.mass[1] as f64, None)?;
        worksheet.write_number(row, 16, entry.offset[1] as f64, None)?;
        worksheet.write_number(row, 17, entry.offset1[1] as f64, None)?;
        worksheet.write_number(row, 18, entry.offset2[1] as f64, None)?;
        worksheet.write_number(row, 19, entry.tolerance_bottom[1] as f64, None)?;
        worksheet.write_number(row, 20, entry.tolerance_top[1] as f64, None)?;
        let status = error_matching(&entry.status[1]).await?;
        worksheet.write_string(row, 21, &status.join(","), None)?;

        worksheet.write_number(row, 22, entry.integral[2] as f64, None)?;
        worksheet.write_number(row, 23, entry.mass[2] as f64, None)?;
        worksheet.write_number(row, 24, entry.offset[2] as f64, None)?;
        worksheet.write_number(row, 25, entry.offset1[2] as f64, None)?;
        worksheet.write_number(row, 26, entry.offset2[2] as f64, None)?;
        worksheet.write_number(row, 27, entry.tolerance_bottom[2] as f64, None)?;
        worksheet.write_number(row, 28, entry.tolerance_top[2] as f64, None)?;
        let status = error_matching(&entry.status[2]).await?;
        worksheet.write_string(row, 29, &status.join(","), None)?;

        worksheet.write_number(row, 30, entry.integral[3] as f64, None)?;
        worksheet.write_number(row, 31, entry.mass[3] as f64, None)?;
        worksheet.write_number(row, 32, entry.offset[3] as f64, None)?;
        worksheet.write_number(row, 33, entry.offset1[3] as f64, None)?;
        worksheet.write_number(row, 34, entry.offset2[3] as f64, None)?;
        worksheet.write_number(row, 35, entry.tolerance_bottom[3] as f64, None)?;
        worksheet.write_number(row, 36, entry.tolerance_top[3] as f64, None)?;
        let status = error_matching(&entry.status[3]).await?;
        worksheet.write_string(row, 37, &status.join(","), None)?;

        worksheet.write_number(row, 38, entry.integral[4] as f64, None)?;
        worksheet.write_number(row, 39, entry.mass[4] as f64, None)?;
        worksheet.write_number(row, 40, entry.offset[4] as f64, None)?;
        worksheet.write_number(row, 41, entry.offset1[4] as f64, None)?;
        worksheet.write_number(row, 42, entry.offset2[4] as f64, None)?;
        worksheet.write_number(row, 43, entry.tolerance_bottom[4] as f64, None)?;
        worksheet.write_number(row, 44, entry.tolerance_top[4] as f64, None)?;
        let status = error_matching(&entry.status[4]).await?;
        worksheet.write_string(row, 45, &status.join(","), None)?;
    }

    Ok(())
}

pub async fn store_measurement_data_as_xlsx_6CH(data: &Vec<UdpTag41>,name: &str, ip: &str) -> Result<(), Box<dyn Error>> {
    // Create the workbook and worksheet
    let workbook = Workbook::new(name)?;
    let mut worksheet = workbook.add_worksheet(None)?;

    //let ip = "172.30.1.122";

    // Write headers
    let headers = ["Zeitstempel Erstellt", "Sensor IP", "Fortlaufender Zähler", "Zeitstempel des letzten Offsetabgleichs", "Dauer des letzten Offsetabgleichs", "Zeitstempel Messung",
     "Integral_CH0", "Masse_CHO", "Offsetwert_CH0", "Offsetwert1_CH0", "Offsetwert2_CH0", "Grenze_Masse_unten_CH0", "Grenze_Masse_oben_CH0", "Status_der_Messung_CH0",
     "Integral_CH1", "Masse_CH1", "Offsetwert_CH1", "Offsetwert1_CH1", "Offsetwert2_CH1", "Grenze_Masse_unten_CH1", "Grenze_Masse_oben_CH1", "Status_der_Messung_CH1",
     "Integral_CH2", "Masse_CH2", "Offsetwert_CH2", "Offsetwert1_CH2", "Offsetwert2_CH2", "Grenze_Masse_unten_CH2", "Grenze_Masse_oben_CH2", "Status_der_Messung_CH2",
     "Integral_CH3", "Masse_CH3", "Offsetwert_CH3", "Offsetwert1_CH3", "Offsetwert2_CH3", "Grenze_Masse_unten_CH3", "Grenze_Masse_oben_CH3", "Status_der_Messung_CH3",
     "Integral_CH4", "Masse_CH4", "Offsetwert_CH4", "Offsetwert1_CH4", "Offsetwert2_CH4", "Grenze_Masse_unten_CH4", "Grenze_Masse_oben_CH4", "Status_der_Messung_CH4",
     "Integral_CH5", "Masse_CH5", "Offsetwert_CH5", "Offsetwert1_CH5", "Offsetwert2_CH5", "Grenze_Masse_unten_CH5", "Grenze_Masse_oben_CH5", "Status_der_Messung_CH5"];

    for (col, header) in headers.iter().enumerate() {
        worksheet.write_string(0, col as u16, header, None)?;

    }

    for (i, entry) in data.iter().enumerate() {
        let row = (i + 1) as u32; // Start at the second row
        
        worksheet.write_string(row, 0, &entry.created, None)?;
        worksheet.write_string(row, 1, ip, None)?;
        worksheet.write_number(row, 2, entry.counter as f64, None)?;
        worksheet.write_string(row, 5, &entry.timestamp, None)?;

        worksheet.write_number(row, 6, entry.integral[0] as f64, None)?;
        worksheet.write_number(row, 7, entry.mass[0] as f64, None)?;
        worksheet.write_number(row, 8, entry.offset[0] as f64, None)?;
        worksheet.write_number(row, 9, entry.offset1[0] as f64, None)?;
        worksheet.write_number(row, 10, entry.offset2[0] as f64, None)?;
        worksheet.write_number(row, 11, entry.tolerance_bottom[0] as f64, None)?;
        worksheet.write_number(row, 12, entry.tolerance_top[0] as f64, None)?;
        let status = error_matching(&entry.status[0]).await?;
        worksheet.write_string(row, 13, &status.join(","), None)?;

        worksheet.write_number(row, 14, entry.integral[1] as f64, None)?;
        worksheet.write_number(row, 15, entry.mass[1] as f64, None)?;
        worksheet.write_number(row, 16, entry.offset[1] as f64, None)?;
        worksheet.write_number(row, 17, entry.offset1[1] as f64, None)?;
        worksheet.write_number(row, 18, entry.offset2[1] as f64, None)?;
        worksheet.write_number(row, 19, entry.tolerance_bottom[1] as f64, None)?;
        worksheet.write_number(row, 20, entry.tolerance_top[1] as f64, None)?;
        let status = error_matching(&entry.status[0]).await?;
        worksheet.write_string(row, 21, &status.join(","), None)?;

        worksheet.write_number(row, 22, entry.integral[2] as f64, None)?;
        worksheet.write_number(row, 23, entry.mass[2] as f64, None)?;
        worksheet.write_number(row, 24, entry.offset[2] as f64, None)?;
        worksheet.write_number(row, 25, entry.offset1[2] as f64, None)?;
        worksheet.write_number(row, 26, entry.offset2[2] as f64, None)?;
        worksheet.write_number(row, 27, entry.tolerance_bottom[2] as f64, None)?;
        worksheet.write_number(row, 28, entry.tolerance_top[2] as f64, None)?;
        let status = error_matching(&entry.status[1]).await?;
        worksheet.write_string(row, 29, &status.join(","), None)?;

        worksheet.write_number(row, 30, entry.integral[3] as f64, None)?;
        worksheet.write_number(row, 31, entry.mass[3] as f64, None)?;
        worksheet.write_number(row, 32, entry.offset[3] as f64, None)?;
        worksheet.write_number(row, 33, entry.offset1[3] as f64, None)?;
        worksheet.write_number(row, 34, entry.offset2[3] as f64, None)?;
        worksheet.write_number(row, 35, entry.tolerance_bottom[3] as f64, None)?;
        worksheet.write_number(row, 36, entry.tolerance_top[3] as f64, None)?;
        let status = error_matching(&entry.status[2]).await?;
        worksheet.write_string(row, 37, &status.join(","), None)?;

        worksheet.write_number(row, 38, entry.integral[4] as f64, None)?;
        worksheet.write_number(row, 39, entry.mass[4] as f64, None)?;
        worksheet.write_number(row, 40, entry.offset[4] as f64, None)?;
        worksheet.write_number(row, 41, entry.offset1[4] as f64, None)?;
        worksheet.write_number(row, 42, entry.offset2[4] as f64, None)?;
        worksheet.write_number(row, 43, entry.tolerance_bottom[4] as f64, None)?;
        worksheet.write_number(row, 44, entry.tolerance_top[4] as f64, None)?;
        let status = error_matching(&entry.status[4]).await?;
        worksheet.write_string(row, 45, &status.join(","), None)?;

        worksheet.write_number(row, 46, entry.integral[5] as f64, None)?;
        worksheet.write_number(row, 47, entry.mass[5] as f64, None)?;
        worksheet.write_number(row, 48, entry.offset[5] as f64, None)?;
        worksheet.write_number(row, 49, entry.offset1[5] as f64, None)?;
        worksheet.write_number(row, 50, entry.offset2[5] as f64, None)?;
        worksheet.write_number(row, 51, entry.tolerance_bottom[5] as f64, None)?;
        worksheet.write_number(row, 52, entry.tolerance_top[5] as f64, None)?;
        let status = error_matching(&entry.status[5]).await?;
        worksheet.write_string(row, 53, &status.join(","), None)?;
    }
    Ok(())
}

pub async fn store_measurement_data_as_xlsx_7CH(data: &Vec<UdpTag41>,name: &str, ip: &str) -> Result<(), Box<dyn Error>> {
    // Create the workbook and worksheet
    let workbook = Workbook::new(name)?;
    let mut worksheet = workbook.add_worksheet(None)?;

    //let ip = "172.30.1.122";

    // Write headers
    let headers = ["Zeitstempel Erstellt", "Sensor IP", "Fortlaufender Zähler", "Zeitstempel des letzten Offsetabgleichs", "Dauer des letzten Offsetabgleichs", "Zeitstempel Messung",
     "Integral_CH0", "Masse_CHO", "Offsetwert_CH0", "Offsetwert1_CH0", "Offsetwert2_CH0", "Grenze_Masse_unten_CH0", "Grenze_Masse_oben_CH0", "Status_der_Messung_CH0",
     "Integral_CH1", "Masse_CH1", "Offsetwert_CH1", "Offsetwert1_CH1", "Offsetwert2_CH1", "Grenze_Masse_unten_CH1", "Grenze_Masse_oben_CH1", "Status_der_Messung_CH1",
     "Integral_CH2", "Masse_CH2", "Offsetwert_CH2", "Offsetwert1_CH2", "Offsetwert2_CH2", "Grenze_Masse_unten_CH2", "Grenze_Masse_oben_CH2", "Status_der_Messung_CH2",
     "Integral_CH3", "Masse_CH3", "Offsetwert_CH3", "Offsetwert1_CH3", "Offsetwert2_CH3", "Grenze_Masse_unten_CH3", "Grenze_Masse_oben_CH3", "Status_der_Messung_CH3",
     "Integral_CH4", "Masse_CH4", "Offsetwert_CH4", "Offsetwert1_CH4", "Offsetwert2_CH4", "Grenze_Masse_unten_CH4", "Grenze_Masse_oben_CH4", "Status_der_Messung_CH4",
     "Integral_CH5", "Masse_CH5", "Offsetwert_CH5", "Offsetwert1_CH5", "Offsetwert2_CH5", "Grenze_Masse_unten_CH5", "Grenze_Masse_oben_CH5", "Status_der_Messung_CH5",
     "Integral_CH6", "Masse_CH6", "Offsetwert_CH6", "Offsetwert1_CH6", "Offsetwert2_CH6", "Grenze_Masse_unten_CH6", "Grenze_Masse_oben_CH6", "Status_der_Messung_CH6"];

    for (col, header) in headers.iter().enumerate() {
        worksheet.write_string(0, col as u16, header, None)?;

    }

    for (i, entry) in data.iter().enumerate() {
        let row = (i + 1) as u32; // Start at the second row
        
        worksheet.write_string(row, 0, &entry.created, None)?;
        worksheet.write_string(row, 1, ip, None)?;
        worksheet.write_number(row, 2, entry.counter as f64, None)?;
        worksheet.write_string(row, 5, &entry.timestamp, None)?;

        worksheet.write_number(row, 6, entry.integral[0] as f64, None)?;
        worksheet.write_number(row, 7, entry.mass[0] as f64, None)?;
        worksheet.write_number(row, 8, entry.offset[0] as f64, None)?;
        worksheet.write_number(row, 9, entry.offset1[0] as f64, None)?;
        worksheet.write_number(row, 10, entry.offset2[0] as f64, None)?;
        worksheet.write_number(row, 11, entry.tolerance_bottom[0] as f64, None)?;
        worksheet.write_number(row, 12, entry.tolerance_top[0] as f64, None)?;
        worksheet.write_string(row, 13, &entry.status[0][0], None)?;
        let status = error_matching(&entry.status[0]).await?;
        worksheet.write_string(row, 13, &status.join(","), None)?;

        worksheet.write_number(row, 14, entry.integral[1] as f64, None)?;
        worksheet.write_number(row, 15, entry.mass[1] as f64, None)?;
        worksheet.write_number(row, 16, entry.offset[1] as f64, None)?;
        worksheet.write_number(row, 17, entry.offset1[1] as f64, None)?;
        worksheet.write_number(row, 18, entry.offset2[1] as f64, None)?;
        worksheet.write_number(row, 19, entry.tolerance_bottom[1] as f64, None)?;
        worksheet.write_number(row, 20, entry.tolerance_top[1] as f64, None)?;
        worksheet.write_string(row, 21, &entry.status[1][0], None)?;
        let status = error_matching(&entry.status[1]).await?;
        worksheet.write_string(row, 22, &status.join(","), None)?;

        worksheet.write_number(row, 22, entry.integral[2] as f64, None)?;
        worksheet.write_number(row, 23, entry.mass[2] as f64, None)?;
        worksheet.write_number(row, 24, entry.offset[2] as f64, None)?;
        worksheet.write_number(row, 25, entry.offset1[2] as f64, None)?;
        worksheet.write_number(row, 26, entry.offset2[2] as f64, None)?;
        worksheet.write_number(row, 27, entry.tolerance_bottom[2] as f64, None)?;
        worksheet.write_number(row, 28, entry.tolerance_top[2] as f64, None)?;
        let status = error_matching(&entry.status[2]).await?;
        worksheet.write_string(row, 29, &status.join(","), None)?;

        worksheet.write_number(row, 30, entry.integral[3] as f64, None)?;
        worksheet.write_number(row, 31, entry.mass[3] as f64, None)?;
        worksheet.write_number(row, 32, entry.offset[3] as f64, None)?;
        worksheet.write_number(row, 33, entry.offset1[3] as f64, None)?;
        worksheet.write_number(row, 34, entry.offset2[3] as f64, None)?;
        worksheet.write_number(row, 35, entry.tolerance_bottom[3] as f64, None)?;
        worksheet.write_number(row, 36, entry.tolerance_top[3] as f64, None)?;
        worksheet.write_string(row, 37, &entry.status[3][0], None)?;
        let status = error_matching(&entry.status[3]).await?;
        worksheet.write_string(row, 37, &status.join(","), None)?;

        worksheet.write_number(row, 38, entry.integral[4] as f64, None)?;
        worksheet.write_number(row, 39, entry.mass[4] as f64, None)?;
        worksheet.write_number(row, 40, entry.offset[4] as f64, None)?;
        worksheet.write_number(row, 41, entry.offset1[4] as f64, None)?;
        worksheet.write_number(row, 42, entry.offset2[4] as f64, None)?;
        worksheet.write_number(row, 43, entry.tolerance_bottom[4] as f64, None)?;
        worksheet.write_number(row, 44, entry.tolerance_top[4] as f64, None)?;
        let status = error_matching(&entry.status[4]).await?;
        worksheet.write_string(row, 45, &status.join(","), None)?;

        worksheet.write_number(row, 46, entry.integral[5] as f64, None)?;
        worksheet.write_number(row, 47, entry.mass[5] as f64, None)?;
        worksheet.write_number(row, 48, entry.offset[5] as f64, None)?;
        worksheet.write_number(row, 49, entry.offset1[5] as f64, None)?;
        worksheet.write_number(row, 50, entry.offset2[5] as f64, None)?;
        worksheet.write_number(row, 51, entry.tolerance_bottom[5] as f64, None)?;
        worksheet.write_number(row, 52, entry.tolerance_top[5] as f64, None)?;
        let status = error_matching(&entry.status[5]).await?;
        worksheet.write_string(row, 53, &status.join(","), None)?;

        worksheet.write_number(row, 54, entry.integral[6] as f64, None)?;
        worksheet.write_number(row, 55, entry.mass[6] as f64, None)?;
        worksheet.write_number(row, 56, entry.offset[6] as f64, None)?;
        worksheet.write_number(row, 57, entry.offset1[6] as f64, None)?;
        worksheet.write_number(row, 58, entry.offset2[6] as f64, None)?;
        worksheet.write_number(row, 59, entry.tolerance_bottom[6] as f64, None)?;
        worksheet.write_number(row, 60, entry.tolerance_top[6] as f64, None)?;
        let status = error_matching(&entry.status[6]).await?;
        worksheet.write_string(row, 61, &status.join(","), None)?;

    }
    Ok(())
}

pub async fn store_measurement_data_as_xlsx_8CH(data: &Vec<UdpTag41>,name: &str, ip: &str) -> Result<(), Box<dyn Error>> {
    // Create the workbook and worksheet
    let workbook = Workbook::new(name)?;
    let mut worksheet = workbook.add_worksheet(None)?;

    //let ip = "172.30.1.122";

    // Write headers
    let headers = ["Zeitstempel Erstellt", "Sensor IP", "Fortlaufender Zähler", "Zeitstempel des letzten Offsetabgleichs", "Dauer des letzten Offsetabgleichs", "Zeitstempel Messung",
     "Integral_CH0", "Masse_CHO", "Offsetwert_CH0", "Offsetwert1_CH0", "Offsetwert2_CH0", "Grenze_Masse_unten_CH0", "Grenze_Masse_oben_CH0", "Status_der_Messung_CH0",
     "Integral_CH1", "Masse_CH1", "Offsetwert_CH1", "Offsetwert1_CH1", "Offsetwert2_CH1", "Grenze_Masse_unten_CH1", "Grenze_Masse_oben_CH1", "Status_der_Messung_CH1",
     "Integral_CH2", "Masse_CH2", "Offsetwert_CH2", "Offsetwert1_CH2", "Offsetwert2_CH2", "Grenze_Masse_unten_CH2", "Grenze_Masse_oben_CH2", "Status_der_Messung_CH2",
     "Integral_CH3", "Masse_CH3", "Offsetwert_CH3", "Offsetwert1_CH3", "Offsetwert2_CH3", "Grenze_Masse_unten_CH3", "Grenze_Masse_oben_CH3", "Status_der_Messung_CH3",
     "Integral_CH4", "Masse_CH4", "Offsetwert_CH4", "Offsetwert1_CH4", "Offsetwert2_CH4", "Grenze_Masse_unten_CH4", "Grenze_Masse_oben_CH4", "Status_der_Messung_CH4",
     "Integral_CH5", "Masse_CH5", "Offsetwert_CH5", "Offsetwert1_CH5", "Offsetwert2_CH5", "Grenze_Masse_unten_CH5", "Grenze_Masse_oben_CH5", "Status_der_Messung_CH5",
     "Integral_CH6", "Masse_CH6", "Offsetwert_CH6", "Offsetwert1_CH6", "Offsetwert2_CH6", "Grenze_Masse_unten_CH6", "Grenze_Masse_oben_CH6", "Status_der_Messung_CH6",
     "Integral_CH7", "Masse_CH7", "Offsetwert_CH7", "Offsetwert1_CH7", "Offsetwert2_CH7", "Grenze_Masse_unten_CH7", "Grenze_Masse_oben_CH7", "Status_der_Messung_CH7"];

    for (col, header) in headers.iter().enumerate() {
        worksheet.write_string(0, col as u16, header, None)?;

    }

    for (i, entry) in data.iter().enumerate() {
        let row = (i + 1) as u32; // Start at the second row
        
        worksheet.write_string(row, 0, &entry.created, None)?;
        worksheet.write_string(row, 1, ip, None)?;
        worksheet.write_number(row, 2, entry.counter as f64, None)?;
        worksheet.write_string(row, 5, &entry.timestamp, None)?;

        worksheet.write_number(row, 6, entry.integral[0] as f64, None)?;
        worksheet.write_number(row, 7, entry.mass[0] as f64, None)?;
        worksheet.write_number(row, 8, entry.offset[0] as f64, None)?;
        worksheet.write_number(row, 9, entry.offset1[0] as f64, None)?;
        worksheet.write_number(row, 10, entry.offset2[0] as f64, None)?;
        worksheet.write_number(row, 11, entry.tolerance_bottom[0] as f64, None)?;
        worksheet.write_number(row, 12, entry.tolerance_top[0] as f64, None)?;
        let status = error_matching(&entry.status[0]).await?;
        worksheet.write_string(row, 13, &status.join(","), None)?;

        worksheet.write_number(row, 14, entry.integral[1] as f64, None)?;
        worksheet.write_number(row, 15, entry.mass[1] as f64, None)?;
        worksheet.write_number(row, 16, entry.offset[1] as f64, None)?;
        worksheet.write_number(row, 17, entry.offset1[1] as f64, None)?;
        worksheet.write_number(row, 18, entry.offset2[1] as f64, None)?;
        worksheet.write_number(row, 19, entry.tolerance_bottom[1] as f64, None)?;
        worksheet.write_number(row, 20, entry.tolerance_top[1] as f64, None)?;
        let status = error_matching(&entry.status[1]).await?;
        worksheet.write_string(row, 21, &status.join(","), None)?;


        worksheet.write_number(row, 22, entry.integral[2] as f64, None)?;
        worksheet.write_number(row, 23, entry.mass[2] as f64, None)?;
        worksheet.write_number(row, 24, entry.offset[2] as f64, None)?;
        worksheet.write_number(row, 25, entry.offset1[2] as f64, None)?;
        worksheet.write_number(row, 26, entry.offset2[2] as f64, None)?;
        worksheet.write_number(row, 27, entry.tolerance_bottom[2] as f64, None)?;
        worksheet.write_number(row, 28, entry.tolerance_top[2] as f64, None)?;
        let status = error_matching(&entry.status[2]).await?;
        worksheet.write_string(row, 29, &status.join(","), None)?;

        worksheet.write_number(row, 30, entry.integral[3] as f64, None)?;
        worksheet.write_number(row, 31, entry.mass[3] as f64, None)?;
        worksheet.write_number(row, 32, entry.offset[3] as f64, None)?;
        worksheet.write_number(row, 33, entry.offset1[3] as f64, None)?;
        worksheet.write_number(row, 34, entry.offset2[3] as f64, None)?;
        worksheet.write_number(row, 35, entry.tolerance_bottom[3] as f64, None)?;
        worksheet.write_number(row, 36, entry.tolerance_top[3] as f64, None)?;
        let status = error_matching(&entry.status[3]).await?;
        worksheet.write_string(row, 37, &status.join(","), None)?;

        worksheet.write_number(row, 38, entry.integral[4] as f64, None)?;
        worksheet.write_number(row, 39, entry.mass[4] as f64, None)?;
        worksheet.write_number(row, 40, entry.offset[4] as f64, None)?;
        worksheet.write_number(row, 41, entry.offset1[4] as f64, None)?;
        worksheet.write_number(row, 42, entry.offset2[4] as f64, None)?;
        worksheet.write_number(row, 43, entry.tolerance_bottom[4] as f64, None)?;
        worksheet.write_number(row, 44, entry.tolerance_top[4] as f64, None)?;
        let status = error_matching(&entry.status[4]).await?;
        worksheet.write_string(row, 45, &status.join(","), None)?;


        worksheet.write_number(row, 46, entry.integral[5] as f64, None)?;
        worksheet.write_number(row, 47, entry.mass[5] as f64, None)?;
        worksheet.write_number(row, 48, entry.offset[5] as f64, None)?;
        worksheet.write_number(row, 49, entry.offset1[5] as f64, None)?;
        worksheet.write_number(row, 50, entry.offset2[5] as f64, None)?;
        worksheet.write_number(row, 51, entry.tolerance_bottom[5] as f64, None)?;
        worksheet.write_number(row, 52, entry.tolerance_top[5] as f64, None)?;
        let status = error_matching(&entry.status[5]).await?;
        worksheet.write_string(row, 53, &status.join(","), None)?;

        worksheet.write_number(row, 54, entry.integral[6] as f64, None)?;
        worksheet.write_number(row, 55, entry.mass[6] as f64, None)?;
        worksheet.write_number(row, 56, entry.offset[6] as f64, None)?;
        worksheet.write_number(row, 57, entry.offset1[6] as f64, None)?;
        worksheet.write_number(row, 58, entry.offset2[6] as f64, None)?;
        worksheet.write_number(row, 59, entry.tolerance_bottom[6] as f64, None)?;
        worksheet.write_number(row, 60, entry.tolerance_top[6] as f64, None)?;
        let status = error_matching(&entry.status[6]).await?;
        worksheet.write_string(row, 61, &status.join(","), None)?;

        worksheet.write_number(row, 62, entry.integral[7] as f64, None)?;
        worksheet.write_number(row, 63, entry.mass[7] as f64, None)?;
        worksheet.write_number(row, 64, entry.offset[7] as f64, None)?;
        worksheet.write_number(row, 65, entry.offset1[7] as f64, None)?;
        worksheet.write_number(row, 66, entry.offset2[7] as f64, None)?;
        worksheet.write_number(row, 67, entry.tolerance_bottom[7] as f64, None)?;
        worksheet.write_number(row, 68, entry.tolerance_top[7] as f64, None)?;
        let status = error_matching(&entry.status[7]).await?;
        worksheet.write_string(row, 69, &status.join(","), None)?;
    }
    Ok(())
}

pub async fn store_measurement_data_as_xlsx_9CH(data: &Vec<UdpTag41>,name: &str, ip: &str) -> Result<(), Box<dyn Error>> {
    // Create the workbook and worksheet
    let workbook = Workbook::new(name)?;
    let mut worksheet = workbook.add_worksheet(None)?;

    //let ip = "172.30.1.122";

    // Write headers
    let headers = ["Zeitstempel Erstellt", "Sensor IP", "Fortlaufender Zähler", "Zeitstempel des letzten Offsetabgleichs", "Dauer des letzten Offsetabgleichs", "Zeitstempel Messung",
     "Integral_CH0", "Masse_CHO", "Offsetwert_CH0", "Offsetwert1_CH0", "Offsetwert2_CH0", "Grenze_Masse_unten_CH0", "Grenze_Masse_oben_CH0", "Status_der_Messung_CH0",
     "Integral_CH1", "Masse_CH1", "Offsetwert_CH1", "Offsetwert1_CH1", "Offsetwert2_CH1", "Grenze_Masse_unten_CH1", "Grenze_Masse_oben_CH1", "Status_der_Messung_CH1",
     "Integral_CH2", "Masse_CH2", "Offsetwert_CH2", "Offsetwert1_CH2", "Offsetwert2_CH2", "Grenze_Masse_unten_CH2", "Grenze_Masse_oben_CH2", "Status_der_Messung_CH2",
     "Integral_CH3", "Masse_CH3", "Offsetwert_CH3", "Offsetwert1_CH3", "Offsetwert2_CH3", "Grenze_Masse_unten_CH3", "Grenze_Masse_oben_CH3", "Status_der_Messung_CH3",
     "Integral_CH4", "Masse_CH4", "Offsetwert_CH4", "Offsetwert1_CH4", "Offsetwert2_CH4", "Grenze_Masse_unten_CH4", "Grenze_Masse_oben_CH4", "Status_der_Messung_CH4",
     "Integral_CH5", "Masse_CH5", "Offsetwert_CH5", "Offsetwert1_CH5", "Offsetwert2_CH5", "Grenze_Masse_unten_CH5", "Grenze_Masse_oben_CH5", "Status_der_Messung_CH5",
     "Integral_CH6", "Masse_CH6", "Offsetwert_CH6", "Offsetwert1_CH6", "Offsetwert2_CH6", "Grenze_Masse_unten_CH6", "Grenze_Masse_oben_CH6", "Status_der_Messung_CH6",
     "Integral_CH7", "Masse_CH7", "Offsetwert_CH7", "Offsetwert1_CH7", "Offsetwert2_CH7", "Grenze_Masse_unten_CH7", "Grenze_Masse_oben_CH7", "Status_der_Messung_CH7",
     "Integral_CH8", "Masse_CH8", "Offsetwert_CH8", "Offsetwert1_CH8", "Offsetwert2_CH8", "Grenze_Masse_unten_CH8", "Grenze_Masse_oben_CH8", "Status_der_Messung_CH8"];

    for (col, header) in headers.iter().enumerate() {
        worksheet.write_string(0, col as u16, header, None)?;

    }

    for (i, entry) in data.iter().enumerate() {
        let row = (i + 1) as u32; // Start at the second row
        
        worksheet.write_string(row, 0, &entry.created, None)?;
        worksheet.write_string(row, 1, ip, None)?;
        worksheet.write_number(row, 2, entry.counter as f64, None)?;
        worksheet.write_string(row, 5, &entry.timestamp, None)?;

        worksheet.write_number(row, 6, entry.integral[0] as f64, None)?;
        worksheet.write_number(row, 7, entry.mass[0] as f64, None)?;
        worksheet.write_number(row, 8, entry.offset[0] as f64, None)?;
        worksheet.write_number(row, 9, entry.offset1[0] as f64, None)?;
        worksheet.write_number(row, 10, entry.offset2[0] as f64, None)?;
        worksheet.write_number(row, 11, entry.tolerance_bottom[0] as f64, None)?;
        worksheet.write_number(row, 12, entry.tolerance_top[0] as f64, None)?;
        worksheet.write_string(row, 13, &entry.status[0][0], None)?;
        let status = error_matching(&entry.status[0]).await?;
        worksheet.write_string(row, 13, &status.join(","), None)?;

        worksheet.write_number(row, 14, entry.integral[1] as f64, None)?;
        worksheet.write_number(row, 15, entry.mass[1] as f64, None)?;
        worksheet.write_number(row, 16, entry.offset[1] as f64, None)?;
        worksheet.write_number(row, 17, entry.offset1[1] as f64, None)?;
        worksheet.write_number(row, 18, entry.offset2[1] as f64, None)?;
        worksheet.write_number(row, 19, entry.tolerance_bottom[1] as f64, None)?;
        worksheet.write_number(row, 20, entry.tolerance_top[1] as f64, None)?;
        let status = error_matching(&entry.status[1]).await?;
        worksheet.write_string(row, 21, &status.join(","), None)?;

        worksheet.write_number(row, 22, entry.integral[2] as f64, None)?;
        worksheet.write_number(row, 23, entry.mass[2] as f64, None)?;
        worksheet.write_number(row, 24, entry.offset[2] as f64, None)?;
        worksheet.write_number(row, 25, entry.offset1[2] as f64, None)?;
        worksheet.write_number(row, 26, entry.offset2[2] as f64, None)?;
        worksheet.write_number(row, 27, entry.tolerance_bottom[2] as f64, None)?;
        worksheet.write_number(row, 28, entry.tolerance_top[2] as f64, None)?;
        let status = error_matching(&entry.status[2]).await?;
        worksheet.write_string(row, 29, &status.join(","), None)?;

        worksheet.write_number(row, 30, entry.integral[3] as f64, None)?;
        worksheet.write_number(row, 31, entry.mass[3] as f64, None)?;
        worksheet.write_number(row, 32, entry.offset[3] as f64, None)?;
        worksheet.write_number(row, 33, entry.offset1[3] as f64, None)?;
        worksheet.write_number(row, 34, entry.offset2[3] as f64, None)?;
        worksheet.write_number(row, 35, entry.tolerance_bottom[3] as f64, None)?;
        worksheet.write_number(row, 36, entry.tolerance_top[3] as f64, None)?;

        let status = error_matching(&entry.status[3]).await?;
        worksheet.write_string(row, 37, &status.join(","), None)?;

        worksheet.write_number(row, 38, entry.integral[4] as f64, None)?;
        worksheet.write_number(row, 39, entry.mass[4] as f64, None)?;
        worksheet.write_number(row, 40, entry.offset[4] as f64, None)?;
        worksheet.write_number(row, 41, entry.offset1[4] as f64, None)?;
        worksheet.write_number(row, 42, entry.offset2[4] as f64, None)?;
        worksheet.write_number(row, 43, entry.tolerance_bottom[4] as f64, None)?;
        worksheet.write_number(row, 44, entry.tolerance_top[4] as f64, None)?;
        let status = error_matching(&entry.status[4]).await?;
        worksheet.write_string(row, 45, &status.join(","), None)?;

        worksheet.write_number(row, 46, entry.integral[5] as f64, None)?;
        worksheet.write_number(row, 47, entry.mass[5] as f64, None)?;
        worksheet.write_number(row, 48, entry.offset[5] as f64, None)?;
        worksheet.write_number(row, 49, entry.offset1[5] as f64, None)?;
        worksheet.write_number(row, 50, entry.offset2[5] as f64, None)?;
        worksheet.write_number(row, 51, entry.tolerance_bottom[5] as f64, None)?;
        worksheet.write_number(row, 52, entry.tolerance_top[5] as f64, None)?;
        let status = error_matching(&entry.status[5]).await?;
        worksheet.write_string(row, 53, &status.join(","), None)?;

        worksheet.write_number(row, 54, entry.integral[6] as f64, None)?;
        worksheet.write_number(row, 55, entry.mass[6] as f64, None)?;
        worksheet.write_number(row, 56, entry.offset[6] as f64, None)?;
        worksheet.write_number(row, 57, entry.offset1[6] as f64, None)?;
        worksheet.write_number(row, 58, entry.offset2[6] as f64, None)?;
        worksheet.write_number(row, 59, entry.tolerance_bottom[6] as f64, None)?;
        worksheet.write_number(row, 60, entry.tolerance_top[6] as f64, None)?;
        let status = error_matching(&entry.status[6]).await?;
        worksheet.write_string(row, 61, &status.join(","), None)?;

        worksheet.write_number(row, 62, entry.integral[7] as f64, None)?;
        worksheet.write_number(row, 63, entry.mass[7] as f64, None)?;
        worksheet.write_number(row, 64, entry.offset[7] as f64, None)?;
        worksheet.write_number(row, 65, entry.offset1[7] as f64, None)?;
        worksheet.write_number(row, 66, entry.offset2[7] as f64, None)?;
        worksheet.write_number(row, 67, entry.tolerance_bottom[7] as f64, None)?;
        worksheet.write_number(row, 68, entry.tolerance_top[7] as f64, None)?;
        let status = error_matching(&entry.status[7]).await?;
        worksheet.write_string(row, 69, &status.join(","), None)?;

        worksheet.write_number(row, 70, entry.integral[8] as f64, None)?;
        worksheet.write_number(row, 71, entry.mass[8] as f64, None)?;
        worksheet.write_number(row, 72, entry.offset[8] as f64, None)?;
        worksheet.write_number(row, 73, entry.offset1[8] as f64, None)?;
        worksheet.write_number(row, 74, entry.offset2[8] as f64, None)?;
        worksheet.write_number(row, 75, entry.tolerance_bottom[8] as f64, None)?;
        worksheet.write_number(row, 76, entry.tolerance_top[8] as f64, None)?;
        let status = error_matching(&entry.status[8]).await?;
        worksheet.write_string(row, 77, &status.join(","), None)?;
    };
    
    Ok(())
}

pub async fn store_measurement_data_as_xlsx_10CH(data: &Vec<UdpTag41>,name: &str, ip: &str) -> Result<(), Box<dyn Error>> {
    // Create the workbook and worksheet
    let workbook = Workbook::new(name)?;
    let mut worksheet = workbook.add_worksheet(None)?;

    //let ip: &str = "172.30.1.122";

    // Write headers
    let headers = ["Zeitstempel Erstellt", "Sensor IP", "Fortlaufender Zähler", "Zeitstempel des letzten Offsetabgleichs", "Dauer des letzten Offsetabgleichs", "Zeitstempel Messung",
     "Integral_CH0", "Masse_CHO", "Offsetwert_CH0", "Offsetwert1_CH0", "Offsetwert2_CH0", "Grenze_Masse_unten_CH0", "Grenze_Masse_oben_CH0", "Status_der_Messung_CH0",
     "Integral_CH1", "Masse_CH1", "Offsetwert_CH1", "Offsetwert1_CH1", "Offsetwert2_CH1", "Grenze_Masse_unten_CH1", "Grenze_Masse_oben_CH1", "Status_der_Messung_CH1",
     "Integral_CH2", "Masse_CH2", "Offsetwert_CH2", "Offsetwert1_CH2", "Offsetwert2_CH2", "Grenze_Masse_unten_CH2", "Grenze_Masse_oben_CH2", "Status_der_Messung_CH2",
     "Integral_CH3", "Masse_CH3", "Offsetwert_CH3", "Offsetwert1_CH3", "Offsetwert2_CH3", "Grenze_Masse_unten_CH3", "Grenze_Masse_oben_CH3", "Status_der_Messung_CH3",
     "Integral_CH4", "Masse_CH4", "Offsetwert_CH4", "Offsetwert1_CH4", "Offsetwert2_CH4", "Grenze_Masse_unten_CH4", "Grenze_Masse_oben_CH4", "Status_der_Messung_CH4",
     "Integral_CH5", "Masse_CH5", "Offsetwert_CH5", "Offsetwert1_CH5", "Offsetwert2_CH5", "Grenze_Masse_unten_CH5", "Grenze_Masse_oben_CH5", "Status_der_Messung_CH5",
     "Integral_CH6", "Masse_CH6", "Offsetwert_CH6", "Offsetwert1_CH6", "Offsetwert2_CH6", "Grenze_Masse_unten_CH6", "Grenze_Masse_oben_CH6", "Status_der_Messung_CH6",
     "Integral_CH7", "Masse_CH7", "Offsetwert_CH7", "Offsetwert1_CH7", "Offsetwert2_CH7", "Grenze_Masse_unten_CH7", "Grenze_Masse_oben_CH7", "Status_der_Messung_CH7",
     "Integral_CH8", "Masse_CH8", "Offsetwert_CH8", "Offsetwert1_CH8", "Offsetwert2_CH8", "Grenze_Masse_unten_CH8", "Grenze_Masse_oben_CH8", "Status_der_Messung_CH8",
     "Integral_CH9", "Masse_CH9", "Offsetwert_CH9", "Offsetwert1_CH9", "Offsetwert2_CH9", "Grenze_Masse_unten_CH9", "Grenze_Masse_oben_CH9", "Status_der_Messung_CH9"];

    for (col, header) in headers.iter().enumerate() {
        worksheet.write_string(0, col as u16, header, None)?;

    }

    for (i, entry) in data.iter().enumerate() {
        let row = (i + 1) as u32; // Start at the second row
        
        worksheet.write_string(row, 0, &entry.created, None)?;
        worksheet.write_string(row, 1, ip, None)?;
        worksheet.write_number(row, 2, entry.counter as f64, None)?;
        worksheet.write_string(row, 5, &entry.timestamp, None)?;

        worksheet.write_number(row, 6, entry.integral[0] as f64, None)?;
        worksheet.write_number(row, 7, entry.mass[0] as f64, None)?;
        worksheet.write_number(row, 8, entry.offset[0] as f64, None)?;
        worksheet.write_number(row, 9, entry.offset1[0] as f64, None)?;
        worksheet.write_number(row, 10, entry.offset2[0] as f64, None)?;
        worksheet.write_number(row, 11, entry.tolerance_bottom[0] as f64, None)?;
        worksheet.write_number(row, 12, entry.tolerance_top[0] as f64, None)?;
        let status = error_matching(&entry.status[0]).await?;
        worksheet.write_string(row, 13, &status.join(","), None)?;

        worksheet.write_number(row, 14, entry.integral[1] as f64, None)?;
        worksheet.write_number(row, 15, entry.mass[1] as f64, None)?;
        worksheet.write_number(row, 16, entry.offset[1] as f64, None)?;
        worksheet.write_number(row, 17, entry.offset1[1] as f64, None)?;
        worksheet.write_number(row, 18, entry.offset2[1] as f64, None)?;
        worksheet.write_number(row, 19, entry.tolerance_bottom[1] as f64, None)?;
        worksheet.write_number(row, 20, entry.tolerance_top[1] as f64, None)?;
        let status = error_matching(&entry.status[1]).await?;
        worksheet.write_string(row, 21, &status.join(","), None)?;


        worksheet.write_number(row, 22, entry.integral[2] as f64, None)?;
        worksheet.write_number(row, 23, entry.mass[2] as f64, None)?;
        worksheet.write_number(row, 24, entry.offset[2] as f64, None)?;
        worksheet.write_number(row, 25, entry.offset1[2] as f64, None)?;
        worksheet.write_number(row, 26, entry.offset2[2] as f64, None)?;
        worksheet.write_number(row, 27, entry.tolerance_bottom[2] as f64, None)?;
        worksheet.write_number(row, 28, entry.tolerance_top[2] as f64, None)?;
        let status = error_matching(&entry.status[2]).await?;
        worksheet.write_string(row, 29, &status.join(","), None)?;

        worksheet.write_number(row, 30, entry.integral[3] as f64, None)?;
        worksheet.write_number(row, 31, entry.mass[3] as f64, None)?;
        worksheet.write_number(row, 32, entry.offset[3] as f64, None)?;
        worksheet.write_number(row, 33, entry.offset1[3] as f64, None)?;
        worksheet.write_number(row, 34, entry.offset2[3] as f64, None)?;
        worksheet.write_number(row, 35, entry.tolerance_bottom[3] as f64, None)?;
        worksheet.write_number(row, 36, entry.tolerance_top[3] as f64, None)?;
        let status = error_matching(&entry.status[3]).await?;
        worksheet.write_string(row, 37, &status.join(","), None)?;

        worksheet.write_number(row, 38, entry.integral[4] as f64, None)?;
        worksheet.write_number(row, 39, entry.mass[4] as f64, None)?;
        worksheet.write_number(row, 40, entry.offset[4] as f64, None)?;
        worksheet.write_number(row, 41, entry.offset1[4] as f64, None)?;
        worksheet.write_number(row, 42, entry.offset2[4] as f64, None)?;
        worksheet.write_number(row, 43, entry.tolerance_bottom[4] as f64, None)?;
        worksheet.write_number(row, 44, entry.tolerance_top[4] as f64, None)?;
        let status = error_matching(&entry.status[4]).await?;
        worksheet.write_string(row, 45, &status.join(","), None)?;

        worksheet.write_number(row, 46, entry.integral[5] as f64, None)?;
        worksheet.write_number(row, 47, entry.mass[5] as f64, None)?;
        worksheet.write_number(row, 48, entry.offset[5] as f64, None)?;
        worksheet.write_number(row, 49, entry.offset1[5] as f64, None)?;
        worksheet.write_number(row, 50, entry.offset2[5] as f64, None)?;
        worksheet.write_number(row, 51, entry.tolerance_bottom[5] as f64, None)?;
        worksheet.write_number(row, 52, entry.tolerance_top[5] as f64, None)?;
        let status = error_matching(&entry.status[5]).await?;
        worksheet.write_string(row, 53, &status.join(","), None)?;

        worksheet.write_number(row, 54, entry.integral[6] as f64, None)?;
        worksheet.write_number(row, 55, entry.mass[6] as f64, None)?;
        worksheet.write_number(row, 56, entry.offset[6] as f64, None)?;
        worksheet.write_number(row, 57, entry.offset1[6] as f64, None)?;
        worksheet.write_number(row, 58, entry.offset2[6] as f64, None)?;
        worksheet.write_number(row, 59, entry.tolerance_bottom[6] as f64, None)?;
        worksheet.write_number(row, 60, entry.tolerance_top[6] as f64, None)?;
        let status = error_matching(&entry.status[6]).await?;
        worksheet.write_string(row, 61, &status.join(","), None)?;

        worksheet.write_number(row, 62, entry.integral[7] as f64, None)?;
        worksheet.write_number(row, 63, entry.mass[7] as f64, None)?;
        worksheet.write_number(row, 64, entry.offset[7] as f64, None)?;
        worksheet.write_number(row, 65, entry.offset1[7] as f64, None)?;
        worksheet.write_number(row, 66, entry.offset2[7] as f64, None)?;
        worksheet.write_number(row, 67, entry.tolerance_bottom[7] as f64, None)?;
        worksheet.write_number(row, 68, entry.tolerance_top[7] as f64, None)?;
        let status = error_matching(&entry.status[7]).await?;
        worksheet.write_string(row, 69, &status.join(","), None)?;

        worksheet.write_number(row, 70, entry.integral[8] as f64, None)?;
        worksheet.write_number(row, 71, entry.mass[8] as f64, None)?;
        worksheet.write_number(row, 72, entry.offset[8] as f64, None)?;
        worksheet.write_number(row, 73, entry.offset1[8] as f64, None)?;
        worksheet.write_number(row, 74, entry.offset2[8] as f64, None)?;
        worksheet.write_number(row, 75, entry.tolerance_bottom[8] as f64, None)?;
        worksheet.write_number(row, 76, entry.tolerance_top[8] as f64, None)?;
        let status = error_matching(&entry.status[8]).await?;
        worksheet.write_string(row, 77, &status.join(","), None)?;


        worksheet.write_number(row, 78, entry.integral[9] as f64, None)?;
        worksheet.write_number(row, 79, entry.mass[9] as f64, None)?;
        worksheet.write_number(row, 80, entry.offset[9] as f64, None)?;
        worksheet.write_number(row, 81, entry.offset1[9] as f64, None)?;
        worksheet.write_number(row, 82, entry.offset2[9] as f64, None)?;
        worksheet.write_number(row, 83, entry.tolerance_bottom[9] as f64, None)?;
        worksheet.write_number(row, 84, entry.tolerance_top[9] as f64, None)?;
        let status = error_matching(&entry.status[9]).await?;
        worksheet.write_string(row, 85, &status.join(","), None)?;
    }
    
    Ok(())
}

pub async fn store_measurement_data_as_xlsx_11CH(data: &Vec<UdpTag41>,name: &str, ip: &str) -> Result<(), Box<dyn Error>> {
    // Create the workbook and worksheet
    let workbook = Workbook::new(name)?;
    let mut worksheet = workbook.add_worksheet(None)?;

    //let ip = "172.30.1.122";

    // Write headers
    let headers = ["Zeitstempel Erstellt", "Sensor IP", "Fortlaufender Zähler", "Zeitstempel des letzten Offsetabgleichs", "Dauer des letzten Offsetabgleichs", "Zeitstempel Messung",
     "Integral_CH0", "Masse_CHO", "Offsetwert_CH0", "Offsetwert1_CH0", "Offsetwert2_CH0", "Grenze_Masse_unten_CH0", "Grenze_Masse_oben_CH0", "Status_der_Messung_CH0",
     "Integral_CH1", "Masse_CH1", "Offsetwert_CH1", "Offsetwert1_CH1", "Offsetwert2_CH1", "Grenze_Masse_unten_CH1", "Grenze_Masse_oben_CH1", "Status_der_Messung_CH1",
     "Integral_CH2", "Masse_CH2", "Offsetwert_CH2", "Offsetwert1_CH2", "Offsetwert2_CH2", "Grenze_Masse_unten_CH2", "Grenze_Masse_oben_CH2", "Status_der_Messung_CH2",
     "Integral_CH3", "Masse_CH3", "Offsetwert_CH3", "Offsetwert1_CH3", "Offsetwert2_CH3", "Grenze_Masse_unten_CH3", "Grenze_Masse_oben_CH3", "Status_der_Messung_CH3",
     "Integral_CH4", "Masse_CH4", "Offsetwert_CH4", "Offsetwert1_CH4", "Offsetwert2_CH4", "Grenze_Masse_unten_CH4", "Grenze_Masse_oben_CH4", "Status_der_Messung_CH4",
     "Integral_CH5", "Masse_CH5", "Offsetwert_CH5", "Offsetwert1_CH5", "Offsetwert2_CH5", "Grenze_Masse_unten_CH5", "Grenze_Masse_oben_CH5", "Status_der_Messung_CH5",
     "Integral_CH6", "Masse_CH6", "Offsetwert_CH6", "Offsetwert1_CH6", "Offsetwert2_CH6", "Grenze_Masse_unten_CH6", "Grenze_Masse_oben_CH6", "Status_der_Messung_CH6",
     "Integral_CH7", "Masse_CH7", "Offsetwert_CH7", "Offsetwert1_CH7", "Offsetwert2_CH7", "Grenze_Masse_unten_CH7", "Grenze_Masse_oben_CH7", "Status_der_Messung_CH7",
     "Integral_CH8", "Masse_CH8", "Offsetwert_CH8", "Offsetwert1_CH8", "Offsetwert2_CH8", "Grenze_Masse_unten_CH8", "Grenze_Masse_oben_CH8", "Status_der_Messung_CH8",
     "Integral_CH9", "Masse_CH9", "Offsetwert_CH9", "Offsetwert1_CH9", "Offsetwert2_CH9", "Grenze_Masse_unten_CH9", "Grenze_Masse_oben_CH9", "Status_der_Messung_CH9",
     "Integral_CH10", "Masse_CH10", "Offsetwert_CH10", "Offsetwert1_CH10", "Offsetwert2_CH10", "Grenze_Masse_unten_CH10", "Grenze_Masse_oben_CH10", "Status_der_Messung_CH10"];

    for (col, header) in headers.iter().enumerate() {
        worksheet.write_string(0, col as u16, header, None)?;

    }

    for (i, entry) in data.iter().enumerate() {
        let row = (i + 1) as u32; // Start at the second row
        
        worksheet.write_string(row, 0, &entry.created, None)?;
        worksheet.write_string(row, 1, ip, None)?;
        worksheet.write_number(row, 2, entry.counter as f64, None)?;
        worksheet.write_string(row, 5, &entry.timestamp, None)?;

        worksheet.write_number(row, 6, entry.integral[0] as f64, None)?;
        worksheet.write_number(row, 7, entry.mass[0] as f64, None)?;
        worksheet.write_number(row, 8, entry.offset[0] as f64, None)?;
        worksheet.write_number(row, 9, entry.offset1[0] as f64, None)?;
        worksheet.write_number(row, 10, entry.offset2[0] as f64, None)?;
        worksheet.write_number(row, 11, entry.tolerance_bottom[0] as f64, None)?;
        worksheet.write_number(row, 12, entry.tolerance_top[0] as f64, None)?;
        let status = error_matching(&entry.status[0]).await?;
        worksheet.write_string(row, 13, &status.join(","), None)?;

        worksheet.write_number(row, 14, entry.integral[1] as f64, None)?;
        worksheet.write_number(row, 15, entry.mass[1] as f64, None)?;
        worksheet.write_number(row, 16, entry.offset[1] as f64, None)?;
        worksheet.write_number(row, 17, entry.offset1[1] as f64, None)?;
        worksheet.write_number(row, 18, entry.offset2[1] as f64, None)?;
        worksheet.write_number(row, 19, entry.tolerance_bottom[1] as f64, None)?;
        worksheet.write_number(row, 20, entry.tolerance_top[1] as f64, None)?;
        let status = error_matching(&entry.status[1]).await?;
        worksheet.write_string(row, 21, &status.join(","), None)?;

        worksheet.write_number(row, 22, entry.integral[2] as f64, None)?;
        worksheet.write_number(row, 23, entry.mass[2] as f64, None)?;
        worksheet.write_number(row, 24, entry.offset[2] as f64, None)?;
        worksheet.write_number(row, 25, entry.offset1[2] as f64, None)?;
        worksheet.write_number(row, 26, entry.offset2[2] as f64, None)?;
        worksheet.write_number(row, 27, entry.tolerance_bottom[2] as f64, None)?;
        worksheet.write_number(row, 28, entry.tolerance_top[2] as f64, None)?;
        let status = error_matching(&entry.status[0]).await?;
        worksheet.write_string(row, 29, &status.join(","), None)?;

        worksheet.write_number(row, 30, entry.integral[3] as f64, None)?;
        worksheet.write_number(row, 31, entry.mass[3] as f64, None)?;
        worksheet.write_number(row, 32, entry.offset[3] as f64, None)?;
        worksheet.write_number(row, 33, entry.offset1[3] as f64, None)?;
        worksheet.write_number(row, 34, entry.offset2[3] as f64, None)?;
        worksheet.write_number(row, 35, entry.tolerance_bottom[3] as f64, None)?;
        worksheet.write_number(row, 36, entry.tolerance_top[3] as f64, None)?;
        let status = error_matching(&entry.status[3]).await?;
        worksheet.write_string(row, 37, &status.join(","), None)?;

        worksheet.write_number(row, 38, entry.integral[4] as f64, None)?;
        worksheet.write_number(row, 39, entry.mass[4] as f64, None)?;
        worksheet.write_number(row, 40, entry.offset[4] as f64, None)?;
        worksheet.write_number(row, 41, entry.offset1[4] as f64, None)?;
        worksheet.write_number(row, 42, entry.offset2[4] as f64, None)?;
        worksheet.write_number(row, 43, entry.tolerance_bottom[4] as f64, None)?;
        worksheet.write_number(row, 44, entry.tolerance_top[4] as f64, None)?;
        let status = error_matching(&entry.status[4]).await?;
        worksheet.write_string(row, 44, &status.join(","), None)?;

        worksheet.write_number(row, 46, entry.integral[5] as f64, None)?;
        worksheet.write_number(row, 47, entry.mass[5] as f64, None)?;
        worksheet.write_number(row, 48, entry.offset[5] as f64, None)?;
        worksheet.write_number(row, 49, entry.offset1[5] as f64, None)?;
        worksheet.write_number(row, 50, entry.offset2[5] as f64, None)?;
        worksheet.write_number(row, 51, entry.tolerance_bottom[5] as f64, None)?;
        worksheet.write_number(row, 52, entry.tolerance_top[5] as f64, None)?;
        let status = error_matching(&entry.status[5]).await?;
        worksheet.write_string(row, 53, &status.join(","), None)?;

        worksheet.write_number(row, 54, entry.integral[6] as f64, None)?;
        worksheet.write_number(row, 55, entry.mass[6] as f64, None)?;
        worksheet.write_number(row, 56, entry.offset[6] as f64, None)?;
        worksheet.write_number(row, 57, entry.offset1[6] as f64, None)?;
        worksheet.write_number(row, 58, entry.offset2[6] as f64, None)?;
        worksheet.write_number(row, 59, entry.tolerance_bottom[6] as f64, None)?;
        worksheet.write_number(row, 60, entry.tolerance_top[6] as f64, None)?;
        let status = error_matching(&entry.status[6]).await?;
        worksheet.write_string(row, 61, &status.join(","), None)?;

        worksheet.write_number(row, 62, entry.integral[7] as f64, None)?;
        worksheet.write_number(row, 63, entry.mass[7] as f64, None)?;
        worksheet.write_number(row, 64, entry.offset[7] as f64, None)?;
        worksheet.write_number(row, 65, entry.offset1[7] as f64, None)?;
        worksheet.write_number(row, 66, entry.offset2[7] as f64, None)?;
        worksheet.write_number(row, 67, entry.tolerance_bottom[7] as f64, None)?;
        worksheet.write_number(row, 68, entry.tolerance_top[7] as f64, None)?;
        let status = error_matching(&entry.status[7]).await?;
        worksheet.write_string(row, 69, &status.join(","), None)?;

        worksheet.write_number(row, 70, entry.integral[8] as f64, None)?;
        worksheet.write_number(row, 71, entry.mass[8] as f64, None)?;
        worksheet.write_number(row, 72, entry.offset[8] as f64, None)?;
        worksheet.write_number(row, 73, entry.offset1[8] as f64, None)?;
        worksheet.write_number(row, 74, entry.offset2[8] as f64, None)?;
        worksheet.write_number(row, 75, entry.tolerance_bottom[8] as f64, None)?;
        worksheet.write_number(row, 76, entry.tolerance_top[8] as f64, None)?;
        let status = error_matching(&entry.status[8]).await?;
        worksheet.write_string(row, 77, &status.join(","), None)?;

        worksheet.write_number(row, 78, entry.integral[9] as f64, None)?;
        worksheet.write_number(row, 79, entry.mass[9] as f64, None)?;
        worksheet.write_number(row, 80, entry.offset[9] as f64, None)?;
        worksheet.write_number(row, 81, entry.offset1[9] as f64, None)?;
        worksheet.write_number(row, 82, entry.offset2[9] as f64, None)?;
        worksheet.write_number(row, 83, entry.tolerance_bottom[9] as f64, None)?;
        worksheet.write_number(row, 84, entry.tolerance_top[9] as f64, None)?;
        let status = error_matching(&entry.status[9]).await?;
        worksheet.write_string(row, 85, &status.join(","), None)?;

        worksheet.write_number(row, 86, entry.integral[10] as f64, None)?;
        worksheet.write_number(row, 87, entry.mass[10] as f64, None)?;
        worksheet.write_number(row, 88, entry.offset[10] as f64, None)?;
        worksheet.write_number(row, 89, entry.offset1[10] as f64, None)?;
        worksheet.write_number(row, 90, entry.offset2[10] as f64, None)?;
        worksheet.write_number(row, 91, entry.tolerance_bottom[10] as f64, None)?;
        worksheet.write_number(row, 92, entry.tolerance_top[10] as f64, None)?;
        let status = error_matching(&entry.status[10]).await?;
        worksheet.write_string(row, 93, &status.join(","), None)?;

    }
    Ok(())
}

pub async fn store_measurement_data_as_xlsx_12CH(data: &Vec<UdpTag41>,name: &str, ip: &str) -> Result<(), Box<dyn Error>> {
    // Create the workbook and worksheet
    let workbook = Workbook::new(name)?;
    let mut worksheet = workbook.add_worksheet(None)?;

    //let ip = "172.30.1.122";

    // Write headers
    let headers = ["Zeitstempel Erstellt", "Sensor IP", "Fortlaufender Zähler", "Zeitstempel des letzten Offsetabgleichs", "Dauer des letzten Offsetabgleichs", "Zeitstempel Messung",
     "Integral_CH0", "Masse_CHO", "Offsetwert_CH0", "Offsetwert1_CH0", "Offsetwert2_CH0", "Grenze_Masse_unten_CH0", "Grenze_Masse_oben_CH0", "Status_der_Messung_CH0",
     "Integral_CH1", "Masse_CH1", "Offsetwert_CH1", "Offsetwert1_CH1", "Offsetwert2_CH1", "Grenze_Masse_unten_CH1", "Grenze_Masse_oben_CH1", "Status_der_Messung_CH1",
     "Integral_CH2", "Masse_CH2", "Offsetwert_CH2", "Offsetwert1_CH2", "Offsetwert2_CH2", "Grenze_Masse_unten_CH2", "Grenze_Masse_oben_CH2", "Status_der_Messung_CH2",
     "Integral_CH3", "Masse_CH3", "Offsetwert_CH3", "Offsetwert1_CH3", "Offsetwert2_CH3", "Grenze_Masse_unten_CH3", "Grenze_Masse_oben_CH3", "Status_der_Messung_CH3",
     "Integral_CH4", "Masse_CH4", "Offsetwert_CH4", "Offsetwert1_CH4", "Offsetwert2_CH4", "Grenze_Masse_unten_CH4", "Grenze_Masse_oben_CH4", "Status_der_Messung_CH4",
     "Integral_CH5", "Masse_CH5", "Offsetwert_CH5", "Offsetwert1_CH5", "Offsetwert2_CH5", "Grenze_Masse_unten_CH5", "Grenze_Masse_oben_CH5", "Status_der_Messung_CH5",
     "Integral_CH6", "Masse_CH6", "Offsetwert_CH6", "Offsetwert1_CH6", "Offsetwert2_CH6", "Grenze_Masse_unten_CH6", "Grenze_Masse_oben_CH6", "Status_der_Messung_CH6",
     "Integral_CH7", "Masse_CH7", "Offsetwert_CH7", "Offsetwert1_CH7", "Offsetwert2_CH7", "Grenze_Masse_unten_CH7", "Grenze_Masse_oben_CH7", "Status_der_Messung_CH7",
     "Integral_CH8", "Masse_CH8", "Offsetwert_CH8", "Offsetwert1_CH8", "Offsetwert2_CH8", "Grenze_Masse_unten_CH8", "Grenze_Masse_oben_CH8", "Status_der_Messung_CH8",
     "Integral_CH9", "Masse_CH9", "Offsetwert_CH9", "Offsetwert1_CH9", "Offsetwert2_CH9", "Grenze_Masse_unten_CH9", "Grenze_Masse_oben_CH9", "Status_der_Messung_CH9",
     "Integral_CH10", "Masse_CH10", "Offsetwert_CH10", "Offsetwert1_CH10", "Offsetwert2_CH10", "Grenze_Masse_unten_CH10", "Grenze_Masse_oben_CH10", "Status_der_Messung_CH10",
     "Integral_CH11", "Masse_CH11", "Offsetwert_CH11", "Offsetwert1_CH11", "Offsetwert2_CH11", "Grenze_Masse_unten_CH11", "Grenze_Masse_oben_CH11", "Status_der_Messung_CH11"];

    for (col, header) in headers.iter().enumerate() {
        worksheet.write_string(0, col as u16, header, None)?;

    }

    for (i, entry) in data.iter().enumerate() {
        let row = (i + 1) as u32; // Start at the second row
        
        worksheet.write_string(row, 0, &entry.created, None)?;
        worksheet.write_string(row, 1, ip, None)?;
        worksheet.write_number(row, 2, entry.counter as f64, None)?;
        worksheet.write_string(row, 5, &entry.timestamp, None)?;

        worksheet.write_number(row, 6, entry.integral[0] as f64, None)?;
        worksheet.write_number(row, 7, entry.mass[0] as f64, None)?;
        worksheet.write_number(row, 8, entry.offset[0] as f64, None)?;
        worksheet.write_number(row, 9, entry.offset1[0] as f64, None)?;
        worksheet.write_number(row, 10, entry.offset2[0] as f64, None)?;
        worksheet.write_number(row, 11, entry.tolerance_bottom[0] as f64, None)?;
        worksheet.write_number(row, 12, entry.tolerance_top[0] as f64, None)?;
        let status = error_matching(&entry.status[0]).await?;
        worksheet.write_string(row, 13, &status.join(","), None)?;

        worksheet.write_number(row, 14, entry.integral[1] as f64, None)?;
        worksheet.write_number(row, 15, entry.mass[1] as f64, None)?;
        worksheet.write_number(row, 16, entry.offset[1] as f64, None)?;
        worksheet.write_number(row, 17, entry.offset1[1] as f64, None)?;
        worksheet.write_number(row, 18, entry.offset2[1] as f64, None)?;
        worksheet.write_number(row, 19, entry.tolerance_bottom[1] as f64, None)?;
        worksheet.write_number(row, 20, entry.tolerance_top[1] as f64, None)?;
        let status = error_matching(&entry.status[1]).await?;
        worksheet.write_string(row, 21, &status.join(","), None)?;

        worksheet.write_number(row, 22, entry.integral[2] as f64, None)?;
        worksheet.write_number(row, 23, entry.mass[2] as f64, None)?;
        worksheet.write_number(row, 24, entry.offset[2] as f64, None)?;
        worksheet.write_number(row, 25, entry.offset1[2] as f64, None)?;
        worksheet.write_number(row, 26, entry.offset2[2] as f64, None)?;
        worksheet.write_number(row, 27, entry.tolerance_bottom[2] as f64, None)?;
        worksheet.write_number(row, 28, entry.tolerance_top[2] as f64, None)?;
        let status = error_matching(&entry.status[2]).await?;
        worksheet.write_string(row, 29, &status.join(","), None)?;

        worksheet.write_number(row, 30, entry.integral[3] as f64, None)?;
        worksheet.write_number(row, 31, entry.mass[3] as f64, None)?;
        worksheet.write_number(row, 32, entry.offset[3] as f64, None)?;
        worksheet.write_number(row, 33, entry.offset1[3] as f64, None)?;
        worksheet.write_number(row, 34, entry.offset2[3] as f64, None)?;
        worksheet.write_number(row, 35, entry.tolerance_bottom[3] as f64, None)?;
        worksheet.write_number(row, 36, entry.tolerance_top[3] as f64, None)?;
        let status = error_matching(&entry.status[3]).await?;
        worksheet.write_string(row, 37, &status.join(","), None)?;

        worksheet.write_number(row, 38, entry.integral[4] as f64, None)?;
        worksheet.write_number(row, 39, entry.mass[4] as f64, None)?;
        worksheet.write_number(row, 40, entry.offset[4] as f64, None)?;
        worksheet.write_number(row, 41, entry.offset1[4] as f64, None)?;
        worksheet.write_number(row, 42, entry.offset2[4] as f64, None)?;
        worksheet.write_number(row, 43, entry.tolerance_bottom[4] as f64, None)?;
        worksheet.write_number(row, 44, entry.tolerance_top[4] as f64, None)?;
        let status = error_matching(&entry.status[4]).await?;
        worksheet.write_string(row, 45, &status.join(","), None)?;

        worksheet.write_number(row, 46, entry.integral[5] as f64, None)?;
        worksheet.write_number(row, 47, entry.mass[5] as f64, None)?;
        worksheet.write_number(row, 48, entry.offset[5] as f64, None)?;
        worksheet.write_number(row, 49, entry.offset1[5] as f64, None)?;
        worksheet.write_number(row, 50, entry.offset2[5] as f64, None)?;
        worksheet.write_number(row, 51, entry.tolerance_bottom[5] as f64, None)?;
        worksheet.write_number(row, 52, entry.tolerance_top[5] as f64, None)?;
        let status = error_matching(&entry.status[5]).await?;
        worksheet.write_string(row, 53, &status.join(","), None)?;

        worksheet.write_number(row, 54, entry.integral[6] as f64, None)?;
        worksheet.write_number(row, 55, entry.mass[6] as f64, None)?;
        worksheet.write_number(row, 56, entry.offset[6] as f64, None)?;
        worksheet.write_number(row, 57, entry.offset1[6] as f64, None)?;
        worksheet.write_number(row, 58, entry.offset2[6] as f64, None)?;
        worksheet.write_number(row, 59, entry.tolerance_bottom[6] as f64, None)?;
        worksheet.write_number(row, 60, entry.tolerance_top[6] as f64, None)?;
        let status = error_matching(&entry.status[6]).await?;
        worksheet.write_string(row, 61, &status.join(","), None)?;

        worksheet.write_number(row, 62, entry.integral[7] as f64, None)?;
        worksheet.write_number(row, 63, entry.mass[7] as f64, None)?;
        worksheet.write_number(row, 64, entry.offset[7] as f64, None)?;
        worksheet.write_number(row, 65, entry.offset1[7] as f64, None)?;
        worksheet.write_number(row, 66, entry.offset2[7] as f64, None)?;
        worksheet.write_number(row, 67, entry.tolerance_bottom[7] as f64, None)?;
        worksheet.write_number(row, 68, entry.tolerance_top[7] as f64, None)?;
        let status = error_matching(&entry.status[7]).await?;
        worksheet.write_string(row, 69, &status.join(","), None)?;

        worksheet.write_number(row, 70, entry.integral[8] as f64, None)?;
        worksheet.write_number(row, 71, entry.mass[8] as f64, None)?;
        worksheet.write_number(row, 72, entry.offset[8] as f64, None)?;
        worksheet.write_number(row, 73, entry.offset1[8] as f64, None)?;
        worksheet.write_number(row, 74, entry.offset2[8] as f64, None)?;
        worksheet.write_number(row, 75, entry.tolerance_bottom[8] as f64, None)?;
        worksheet.write_number(row, 76, entry.tolerance_top[8] as f64, None)?;
        let status = error_matching(&entry.status[8]).await?;
        worksheet.write_string(row, 78, &status.join(","), None)?;

        worksheet.write_number(row, 78, entry.integral[9] as f64, None)?;
        worksheet.write_number(row, 79, entry.mass[9] as f64, None)?;
        worksheet.write_number(row, 80, entry.offset[9] as f64, None)?;
        worksheet.write_number(row, 81, entry.offset1[9] as f64, None)?;
        worksheet.write_number(row, 82, entry.offset2[9] as f64, None)?;
        worksheet.write_number(row, 83, entry.tolerance_bottom[9] as f64, None)?;
        worksheet.write_number(row, 84, entry.tolerance_top[9] as f64, None)?;
        let status = error_matching(&entry.status[9]).await?;
        worksheet.write_string(row, 85, &status.join(","), None)?;

        worksheet.write_number(row, 86, entry.integral[10] as f64, None)?;
        worksheet.write_number(row, 87, entry.mass[10] as f64, None)?;
        worksheet.write_number(row, 88, entry.offset[10] as f64, None)?;
        worksheet.write_number(row, 89, entry.offset1[10] as f64, None)?;
        worksheet.write_number(row, 90, entry.offset2[10] as f64, None)?;
        worksheet.write_number(row, 91, entry.tolerance_bottom[10] as f64, None)?;
        worksheet.write_number(row, 92, entry.tolerance_top[10] as f64, None)?;
        let status = error_matching(&entry.status[10]).await?;
        worksheet.write_string(row, 93, &status.join(","), None)?;

        worksheet.write_number(row, 94, entry.integral[11] as f64, None)?;
        worksheet.write_number(row, 95, entry.mass[11] as f64, None)?;
        worksheet.write_number(row, 96, entry.offset[11] as f64, None)?;
        worksheet.write_number(row, 97, entry.offset1[11] as f64, None)?;
        worksheet.write_number(row, 98, entry.offset2[11] as f64, None)?;
        worksheet.write_number(row, 99, entry.tolerance_bottom[11] as f64, None)?;
        worksheet.write_number(row, 100, entry.tolerance_top[11] as f64, None)?;
        let status = error_matching(&entry.status[11]).await?;
        worksheet.write_string(row, 101, &status.join(","), None)?;

    }
    Ok(())
}

pub async fn process_measurement_data(result: Response, ip_address: &str, name: &str, select_type:u8, number_of_channels:u8) -> Result<Vec<(u64, u8, u64, u64, u16, u16, u16, u16, u16, String, String, Vec<String>)>, Box<dyn Error>> {
    let mut data = result;
    let data: Vec<UdpTag41> = match data.take(0) {
        Ok(data) => data,
        Err(e) => {
            println!("Error selecting measurement data: {:?}", e);
            return Err(Box::new(e));
        }
    };
    let ip = ip_address;
    
    match number_of_channels {
        1 => {
            let _ = store_measurement_data_as_xlsx_1CH(&data, name, ip).await?;
        },
        2 => {
            let _ = store_measurement_data_as_xlsx_2CH(&data, name, ip).await?;
        },
        3 => {
            let _ = store_measurement_data_as_xlsx_3CH(&data, name, ip).await?;
        },
        4 => {
            let _ = store_measurement_data_as_xlsx_4CH(&data, name, ip).await?;
        },
        5 => {
            let _ = store_measurement_data_as_xlsx_5CH(&data, name, ip).await?;
        },
        6 => {
            let _ = store_measurement_data_as_xlsx_6CH(&data, name, ip).await?;
        },
        7 => {
            let _ = store_measurement_data_as_xlsx_7CH(&data, name, ip).await?;
        },
        8 => {
            let _ = store_measurement_data_as_xlsx_8CH(&data, name, ip).await?;
        },
        9 => {
            let _ = store_measurement_data_as_xlsx_9CH(&data, name, ip).await?;
        },
        10 => {
            let _ = store_measurement_data_as_xlsx_10CH(&data, name, ip).await?;
        },
        11 => {
            let _ = store_measurement_data_as_xlsx_11CH(&data, name, ip).await?;
        },
        12 => {
            let _ = store_measurement_data_as_xlsx_12CH(&data, name, ip).await?;
        },
        _ => {
            println!("Number of channels not supported");
        }
    }
    if select_type == 1 {
        return Ok(Vec::new());
    }
    
    let exploded_data: Vec<(u64, u8, u64, u64, u16, u16, u16, u16, u16, String, String, Vec<String>)> = data
        .into_iter()
        .flat_map(|tag| {
            tag.channel.into_iter()
                .zip(tag.integral.into_iter()) // Combine the channel and peak vectors
                .zip(tag.mass.into_iter())
                .zip(tag.offset.into_iter())
                .zip(tag.offset1.into_iter())
                .zip(tag.offset2.into_iter())
                .zip(tag.tolerance_bottom.into_iter())
                .zip(tag.tolerance_top.into_iter())
                .zip(tag.status.clone().into_iter())
                .map(move |((((((((channel_value, integral), mass), offset), offset1), offset2), tolerance_bottom), tolerance_top), status)| {
                    (tag.run_counter, channel_value, integral, mass, offset, offset1, offset2, tolerance_bottom, tolerance_top, tag.project.clone(), tag.timestamp.clone(),status)
                })
        })
        .collect();
    Ok(exploded_data)
}

// Main function that uses both helper functions
async fn select_raw_data_async(
    ip: &str,
    port: &str,
    user: &str,
    pw: &str,
    namespace: &str,
    db_name: &str,
    table_name: &str,
    run_id: &str
) -> Result<Vec<(u64, u8, i32, String, u32)>, Box<dyn Error>> {
    let db = connect_to_db(ip, port, user, pw, namespace, db_name).await?;
    let result = query_raw_data(&db, table_name, run_id).await?;
    let data = process_raw_data(result).await?;
    Ok(data)
}

pub async fn query_raw_data(
    db: &Surreal<Client>,
    table_name: &str,
    run_id: &str
) -> Result<surrealdb::Response, Box<dyn Error>>{
    let result_query = format!(
        "SELECT run_counter,channel, data, timestamp FROM {} WHERE run_id = {} ORDER BY run_counter ASC",
        table_name, run_id
    );
    let result = db.query(&result_query).await?;
    Ok(result)
}

pub async fn query_general_information(
    db: &Surreal<Client>,
    table_name: &str,
    run_id: &str
) -> Result<surrealdb::Response, Box<dyn Error>>{
    let result_query = format!(
        "SELECT ip_address, number_of_channels FROM {} WHERE run_id = {}",
        table_name, run_id
    );
    let result = db.query(&result_query).await?;
    Ok(result)
}

pub async fn query_amv_static_info(
    db: &Surreal<Client>,
    table_name: &str,
    run_id: &str
) -> Result<surrealdb::Response, Box<dyn Error>>{
    let result_query = format!(
        "SELECT ip_address, number_of_channels, timestamp FROM {} WHERE run_id = {}",
        table_name, run_id
    );
    let result = db.query(&result_query).await?;
    Ok(result)
}

pub async fn process_raw_data(result: Response) -> Result<Vec<(u64, u8, i32, String, u32)>, Box<dyn Error>> {
    let mut ddata = result;
    let data: Vec<RawData> = match ddata.take(0) {
        Ok(data) => data,
        Err(e) => {
            println!("Error selecting raw data: {:?}", e);
            return Err(Box::new(e));
        }
    };
    let mut exploded_data = Vec::new();
        
    for tag in data {
            let channel_value = tag.channel;
            let run_counter = tag.run_counter;
            let timestamp = tag.timestamp;

            let mut i = 0;
            for data_value in tag.data {
                let duration: u32 = i as u32 * 250;
                let new_timestamp = timestamp + Duration::microseconds(i as i64 * 250);
                i += 1;
                exploded_data.push((run_counter, channel_value, data_value, new_timestamp.clone().to_string(), duration));
            }
        }
        
        Ok(exploded_data)
}
    


    