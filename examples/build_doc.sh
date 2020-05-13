#!/usr/bin/env bash
# BUILD Doc FROM swagger example found in https://github.com/OAI/OpenAPI-Specification/blob/master/examples/v2.0/yaml/


function run_test() {
  name=$1
  clean_after_test=$2
  output=$(echo $name | awk -F'.yaml' '{ print $1 }')".docx"
  echo "Build: $name"

  python swagger-to-docx --swagger https://github.com/OAI/OpenAPI-Specification/raw/master/examples/v2.0/yaml/$name --out $output
  rs=$?
  if [ $rs -eq 0 ]
  then
    echo "Successfully created file"
    if [ ! -z $clean_after_test ]; then
      echo "Remove file: $output"
      rm $output
    fi
  else
    echo "Could not create file"
  fi
}

run_test "petstore-expanded.yaml"
run_test "petstore-minimal.yaml"
run_test "petstore-simple.yaml"
run_test "petstore.yaml"


