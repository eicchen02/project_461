use std::env; //rust stdlib function to get command line args
use std::fs; //rust file library
use std::process;
use std::process::Command; //library to run processes in rust
use std::path::Path;

fn main() {
    //save the command line argument
    let cli_input: Vec<String> = env::args().collect();

    //this will remove output files and locally cloned repos
    clean_up();

    //Obtain flag from ./run (-s, -p, -u)
    let flag: &String = &cli_input[3];

    //take the contents of the file and save into a single string
    let mut url = match fs::read_to_string(&cli_input[2]){
        Ok(url) => url,
        Err(..) => {
            println!("Error reading the input file!\n");
            std::process::exit(1);
        }
    };

    if flag == "-u"{
        //Determing what the input is (either base64 encoded file, or URL)
        let cloned_repo_id = Command::new("python3")
            .arg("input/obtainURL.py")
            .arg(&cli_input[2])
            .output()
            .expect("Err");
        let mut input = String::from_utf8(cloned_repo_id.stdout).unwrap();
        input.pop();
        if input == "-1"{
            println!("Error: package.json does not have a valid URL");
            process::exit(1);
        }
        else{
            url = input;
        }
    }

    //run the rampup calculation (calculate_RampUp)
    let _run_rampup = Command::new("./target/debug/calculate_ramp_up")
        .arg(&url)
        .status()
        .expect("Err"); //runs the rust executable "calculate_RampUp" with the CLI input file

    //if the rampup calculation failed, exit 1 (error message is handled in the calculation code)
    if _run_rampup.success() == false {
        println!("Error calculating rampup!");
        process::exit(1);
    }

    //run the correctness calculation (calculate_Correctness)
    let _run_correctness = Command::new("python3")
        .arg("graphql_api/calculate_Correctness.py")
        .arg(&url)
        .status()
        .expect("Err");

    //if the correctness script didnt return success, exit 1 and print error
    if _run_correctness.success() == false {
        println!("Error calculating correctness!");
        std::process::exit(1);
    }

    //run the bus factor calculation
    let _run_busfactor = Command::new("./target/debug/calculate_bus_factor")
        .arg(&url)
        .status()
        .expect("Err"); //runs the rust executable "calculate_BusFactor" with the CLI input file

    if _run_busfactor.success() == false {
        println!("Error calculating bus factor!");
        process::exit(1);
    }

    //run the updated code score calculation
    let _run_updated_code = Command::new("./target/debug/calculate_updated_code")
        .arg(&url)
        .status()
        .expect("Err"); //runs the rust executable "calculate_UpdatedCode" with the CLI input file

    if _run_updated_code.success() == false {
        println!("Error calculating updated code score!");
        process::exit(1);
    }

    //run the good pinning practice score calculation
    let _run_pinning_practice = Command::new("./target/debug/calculate_pinning_practice")
        .arg(&url)
        .status()
        .expect("Err"); //runs the rust executable "calculate_pinning_practice" with the CLI input file
    
    if _run_pinning_practice.success() == false{
        println!("Error calculating pinning practice score!");
        process::exit(1)
    }
    
    //run the correctness calculation (calculate_Correctness)
    let _run_correctness = Command::new("python3").arg("graphql_api/calculate_Correctness.py").arg(&url).status().expect("Err");

    //if the correctness script didnt return success, exit 1 and print error
    if _run_correctness.success() == false {
        println!("Error calculating correctness!");
        std::process::exit(1);
    }

    //run the responsive maintainer calculation (calculate_ResponsiveMaintainer.py)
    let _run_responsivemaintainer = Command::new("python3")
        .arg("rest_api/calculate_ResponsiveMaintainer.py")
        .arg(&url)
        .status()
        .expect("Err");

    //if the responsive maintainer script didnt return success, exit 1 and print error
    if _run_responsivemaintainer.success() == false {
        println!("Error calculating responsive maintainer!");
        std::process::exit(1);
    }

    //run the license calculation (license.py)
    let _run_license = Command::new("python3")
        .arg("local_cloning/license.py")
        .arg(&url)
        .status()
        .expect("Err");

    //if the license script didnt return success, exit 1 and print error
    if _run_license.success() == false {
        println!("Error calculating license!");
        std::process::exit(1);
    }

    //do logging
    let _set_logs = Command::new("python3")
        .arg("verbosity.py")
        .arg(&url)
        .status()
        .expect("Err");

    //Print results and clean files on -p, save results and not print on -s
    if flag == "-p" || flag == "-u" {
        //print the results (print_results.py)
        let _print_results = Command::new("python3")
            .arg("output/print_results.py")
            .arg(&url)
            .status()
            .expect("Err");

        //if printing results didnt return success, exit 1 and print error
        if _print_results.success() == false {
            println!("Error printing results!");
            std::process::exit(1);
        }

        //if verbosity didnt return success, exit 1 and print error
        if _print_results.success() == false {
            println!("Error in verbosity script!");
            std::process::exit(1);
        }

    }

    //exit 0 on success
    process::exit(0);
}

//this function removes locally cloned repos and output files
fn clean_up() {
    //remove local clone repos
    if Path::new("local_cloning/cloned_repos/").is_dir(){
        let _clean_old_clones = match fs::remove_dir_all("local_cloning/cloned_repos/") {
            Ok(_clean_old_clones) => _clean_old_clones,
            Err(..) => {
                println!("Error cleaning old cloned repos!\n");
                std::process::exit(1);
            }
        };
    }

    //clean output files for each metric
    if Path::new("output/correctness_out.txt").exists(){
        let _clean_correctness = match fs::remove_file("output/correctness_out.txt") {
            Ok(_clean_correctness) => _clean_correctness,
            Err(..) => {
                println!("Error cleaning correctness output!\n");
                std::process::exit(1);
            }
        };
    }

    if Path::new("output/license_out.txt").exists(){
        let _clean_license = match fs::remove_file("output/license_out.txt") {
            Ok(_clean_license) => _clean_license,
            Err(..) => {
                println!("Error cleaning license output!\n");
                std::process::exit(1);
            }
        };
    }

    if Path::new("output/rampup_out.txt").exists(){
        let _clean_rampup = match fs::remove_file("output/rampup_out.txt") {
            Ok(_clean_rampup) => _clean_rampup,
            Err(..) => {
                println!("Error cleaning rampup output!\n");
                std::process::exit(1);
            }
        };
    }

    if Path::new("output/busfactor_out.txt").exists(){
        let _clean_busfactor = match fs::remove_file("output/busfactor_out.txt") {
            Ok(_clean_rampup) => _clean_rampup,
            Err(..) => {
                println!("Error cleaning busfactor output!\n");
                std::process::exit(1);
            }
        };
    }

    if Path::new("output/updatedcode_out.txt").exists(){
        let _clean_updatedcode = match fs::remove_file("output/updatedcode_out.txt") {
            Ok(_clean_rampup) => _clean_rampup,
            Err(..) => {
                println!("Error cleaning updatedcode output!\n");
                std::process::exit(1);
            }
        };
    }

    if Path::new("output/resp_maintain_out.txt").exists(){
        let _clean_respmain = match fs::remove_file("output/resp_maintain_out.txt") {
            Ok(_clean_respmain) => _clean_respmain,
            Err(..) => {
                println!("Error cleaning responsive maintainer output!\n");
                std::process::exit(1);
            }
        };
    }

    if Path::new("output/pinningpractice_out.txt").exists(){
        let _clean_respmain = match fs::remove_file("output/pinningpractice_out.txt") {
            Ok(_clean_respmain) => _clean_respmain,
            Err(..) => {
                println!("Error cleaning pinning practice output!\n");
                std::process::exit(1);
            }
        };
    }
}
