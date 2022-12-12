# put_parameter_args: class to handle kwargs for ssm.put_parameter_args function

class put_parameter_args:
  Name = ""
  Description = ""
  Value = ""
  Type = "SecureString"
  KeyId = ""
  Overwrite = False
  AllowedPattern = ""
  Tags = []
  Tier = "Standard"
  Policies = ""
  DataType = ""

  def __init__(self, props):
    Name = props['Name']
    Value = props['Value']

    if 'Description' in props:
      Description = props['Description']

    if 'Type' in props:
      Type = props['Type']

    if 'KeyId' in props:
      KeyId = props['KeyId']

    if 'Overwrite' in props:
      Overwrite = props['Overwrite']

    if 'AllowedPattern' in props:
      AllowedPattern = props['AllowedPattern']

    if 'Tags' in props:
      Tags = props['Tags']

    if 'Tier' in props:
      Tier = props['Tier']

    if 'Policies' in props:
      Policies = props['Policies']

    if 'DataType' in props:
      DataType = props['DataType']

  def construct_put_parameter_args(self):
    return {
      'Name': Name,
      'Description': Description,
      'Value': Value,
      'Type': Type,
      'KeyId': KeyId,
      'Overwrite': Overwrite,
      'AllowedPattern': AllowedPattern,
      'Tags': Tags,
      'Tier': Tier,
      'Policies': Policies,
      'DataType': DataType
    }

# class Tag:
  # Key = ""
  # Value = ""

  # def __init__(self, key, value):
    # Key = key
    # Value = value

  # def construct_tag(self):
    # return {'Key': Key, 'Value': Value}

