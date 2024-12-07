r'''
# `data_archive_file`

Refer to the Terraform Registry for docs: [`data_archive_file`](https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class DataArchiveFile(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-archive.dataArchiveFile.DataArchiveFile",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file archive_file}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        output_path: builtins.str,
        type: builtins.str,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclude_symlink_directories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        output_file_mode: typing.Optional[builtins.str] = None,
        source: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataArchiveFileSource", typing.Dict[builtins.str, typing.Any]]]]] = None,
        source_content: typing.Optional[builtins.str] = None,
        source_content_filename: typing.Optional[builtins.str] = None,
        source_dir: typing.Optional[builtins.str] = None,
        source_file: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file archive_file} Data Source.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param output_path: The output of the archive file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#output_path DataArchiveFile#output_path}
        :param type: The type of archive to generate. NOTE: ``zip`` and ``tar.gz`` is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#type DataArchiveFile#type}
        :param excludes: Specify files/directories to ignore when reading the ``source_dir``. Supports glob file matching patterns including doublestar/globstar (``**``) patterns. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#excludes DataArchiveFile#excludes}
        :param exclude_symlink_directories: Boolean flag indicating whether symbolically linked directories should be excluded during the creation of the archive. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#exclude_symlink_directories DataArchiveFile#exclude_symlink_directories}
        :param output_file_mode: String that specifies the octal file mode for all archived files. For example: ``"0666"``. Setting this will ensure that cross platform usage of this module will not vary the modes of archived files (and ultimately checksums) resulting in more deterministic behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#output_file_mode DataArchiveFile#output_file_mode}
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#source DataArchiveFile#source}
        :param source_content: Add only this content to the archive with ``source_content_filename`` as the filename. One and only one of ``source``, ``source_content_filename`` (with ``source_content``), ``source_file``, or ``source_dir`` must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#source_content DataArchiveFile#source_content}
        :param source_content_filename: Set this as the filename when using ``source_content``. One and only one of ``source``, ``source_content_filename`` (with ``source_content``), ``source_file``, or ``source_dir`` must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#source_content_filename DataArchiveFile#source_content_filename}
        :param source_dir: Package entire contents of this directory into the archive. One and only one of ``source``, ``source_content_filename`` (with ``source_content``), ``source_file``, or ``source_dir`` must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#source_dir DataArchiveFile#source_dir}
        :param source_file: Package this file into the archive. One and only one of ``source``, ``source_content_filename`` (with ``source_content``), ``source_file``, or ``source_dir`` must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#source_file DataArchiveFile#source_file}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f8174f229f3604133f5c77a80cd25d2977aef1687fff32139249b73dce43cf7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataArchiveFileConfig(
            output_path=output_path,
            type=type,
            excludes=excludes,
            exclude_symlink_directories=exclude_symlink_directories,
            output_file_mode=output_file_mode,
            source=source,
            source_content=source_content,
            source_content_filename=source_content_filename,
            source_dir=source_dir,
            source_file=source_file,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a DataArchiveFile resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataArchiveFile to import.
        :param import_from_id: The id of the existing DataArchiveFile that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataArchiveFile to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__469ab24a096cafd72d07fc9c3aa875004cf4af1d04e6d0ba5bb367da90840577)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataArchiveFileSource", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d003f85638c28bffbd4441abb65c0dc94b23f40ab53f06c48a8d24b28d5f42be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSource", [value]))

    @jsii.member(jsii_name="resetExcludes")
    def reset_excludes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludes", []))

    @jsii.member(jsii_name="resetExcludeSymlinkDirectories")
    def reset_exclude_symlink_directories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeSymlinkDirectories", []))

    @jsii.member(jsii_name="resetOutputFileMode")
    def reset_output_file_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputFileMode", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @jsii.member(jsii_name="resetSourceContent")
    def reset_source_content(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceContent", []))

    @jsii.member(jsii_name="resetSourceContentFilename")
    def reset_source_content_filename(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceContentFilename", []))

    @jsii.member(jsii_name="resetSourceDir")
    def reset_source_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceDir", []))

    @jsii.member(jsii_name="resetSourceFile")
    def reset_source_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceFile", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="outputBase64Sha256")
    def output_base64_sha256(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputBase64Sha256"))

    @builtins.property
    @jsii.member(jsii_name="outputBase64Sha512")
    def output_base64_sha512(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputBase64Sha512"))

    @builtins.property
    @jsii.member(jsii_name="outputMd5")
    def output_md5(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputMd5"))

    @builtins.property
    @jsii.member(jsii_name="outputSha")
    def output_sha(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputSha"))

    @builtins.property
    @jsii.member(jsii_name="outputSha256")
    def output_sha256(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputSha256"))

    @builtins.property
    @jsii.member(jsii_name="outputSha512")
    def output_sha512(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputSha512"))

    @builtins.property
    @jsii.member(jsii_name="outputSize")
    def output_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "outputSize"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "DataArchiveFileSourceList":
        return typing.cast("DataArchiveFileSourceList", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="excludesInput")
    def excludes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeSymlinkDirectoriesInput")
    def exclude_symlink_directories_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "excludeSymlinkDirectoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="outputFileModeInput")
    def output_file_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputFileModeInput"))

    @builtins.property
    @jsii.member(jsii_name="outputPathInput")
    def output_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputPathInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceContentFilenameInput")
    def source_content_filename_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceContentFilenameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceContentInput")
    def source_content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceContentInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceDirInput")
    def source_dir_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceDirInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceFileInput")
    def source_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceFileInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataArchiveFileSource"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataArchiveFileSource"]]], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="excludes")
    def excludes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludes"))

    @excludes.setter
    def excludes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20c4285397b574ace2586d5b7d9c0efed97c37db7016848d04cb03aa64878453)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludeSymlinkDirectories")
    def exclude_symlink_directories(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "excludeSymlinkDirectories"))

    @exclude_symlink_directories.setter
    def exclude_symlink_directories(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63461d561599bf3138af7b713358f4ca8a37731df554faa092adba7988d201e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeSymlinkDirectories", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputFileMode")
    def output_file_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputFileMode"))

    @output_file_mode.setter
    def output_file_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cf0d3fbf6707bec587f4a960cd54edd8e60f917d78b8b942cc183e29c7291d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputFileMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputPath")
    def output_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputPath"))

    @output_path.setter
    def output_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3592643f4a565fac9e7ff8c5189ac2f818943f620f705989325f0070d0f74749)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceContent")
    def source_content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceContent"))

    @source_content.setter
    def source_content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4f7f1c2a67ef2d6cd3380e72c2663d13a07e8a175ff5a4cf7f68c4df802c472)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceContent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceContentFilename")
    def source_content_filename(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceContentFilename"))

    @source_content_filename.setter
    def source_content_filename(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26ddff38facb63d2db815fde82cff0e0559b482fd07b09a7c023eac38911966c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceContentFilename", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceDir")
    def source_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceDir"))

    @source_dir.setter
    def source_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9dfe185d1160c0d01df7661702ee3e6ce0223ba9ffbf6fe85f7c82315c1702f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceDir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceFile")
    def source_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceFile"))

    @source_file.setter
    def source_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cb49ee8a8a77e542ce50503f7116ae685411f0a635d0e39bb93fc1d4c370ceb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60c0778b3789354f6804e1c1ce39630da6b9932c71223ea45e1bb6b723916262)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-archive.dataArchiveFile.DataArchiveFileConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "output_path": "outputPath",
        "type": "type",
        "excludes": "excludes",
        "exclude_symlink_directories": "excludeSymlinkDirectories",
        "output_file_mode": "outputFileMode",
        "source": "source",
        "source_content": "sourceContent",
        "source_content_filename": "sourceContentFilename",
        "source_dir": "sourceDir",
        "source_file": "sourceFile",
    },
)
class DataArchiveFileConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        output_path: builtins.str,
        type: builtins.str,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        exclude_symlink_directories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        output_file_mode: typing.Optional[builtins.str] = None,
        source: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataArchiveFileSource", typing.Dict[builtins.str, typing.Any]]]]] = None,
        source_content: typing.Optional[builtins.str] = None,
        source_content_filename: typing.Optional[builtins.str] = None,
        source_dir: typing.Optional[builtins.str] = None,
        source_file: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param output_path: The output of the archive file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#output_path DataArchiveFile#output_path}
        :param type: The type of archive to generate. NOTE: ``zip`` and ``tar.gz`` is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#type DataArchiveFile#type}
        :param excludes: Specify files/directories to ignore when reading the ``source_dir``. Supports glob file matching patterns including doublestar/globstar (``**``) patterns. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#excludes DataArchiveFile#excludes}
        :param exclude_symlink_directories: Boolean flag indicating whether symbolically linked directories should be excluded during the creation of the archive. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#exclude_symlink_directories DataArchiveFile#exclude_symlink_directories}
        :param output_file_mode: String that specifies the octal file mode for all archived files. For example: ``"0666"``. Setting this will ensure that cross platform usage of this module will not vary the modes of archived files (and ultimately checksums) resulting in more deterministic behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#output_file_mode DataArchiveFile#output_file_mode}
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#source DataArchiveFile#source}
        :param source_content: Add only this content to the archive with ``source_content_filename`` as the filename. One and only one of ``source``, ``source_content_filename`` (with ``source_content``), ``source_file``, or ``source_dir`` must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#source_content DataArchiveFile#source_content}
        :param source_content_filename: Set this as the filename when using ``source_content``. One and only one of ``source``, ``source_content_filename`` (with ``source_content``), ``source_file``, or ``source_dir`` must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#source_content_filename DataArchiveFile#source_content_filename}
        :param source_dir: Package entire contents of this directory into the archive. One and only one of ``source``, ``source_content_filename`` (with ``source_content``), ``source_file``, or ``source_dir`` must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#source_dir DataArchiveFile#source_dir}
        :param source_file: Package this file into the archive. One and only one of ``source``, ``source_content_filename`` (with ``source_content``), ``source_file``, or ``source_dir`` must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#source_file DataArchiveFile#source_file}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__395d6c956a8f6a157e1bf9db0b880a72f8d80755220480442d2acbff968ca74f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument output_path", value=output_path, expected_type=type_hints["output_path"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument excludes", value=excludes, expected_type=type_hints["excludes"])
            check_type(argname="argument exclude_symlink_directories", value=exclude_symlink_directories, expected_type=type_hints["exclude_symlink_directories"])
            check_type(argname="argument output_file_mode", value=output_file_mode, expected_type=type_hints["output_file_mode"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument source_content", value=source_content, expected_type=type_hints["source_content"])
            check_type(argname="argument source_content_filename", value=source_content_filename, expected_type=type_hints["source_content_filename"])
            check_type(argname="argument source_dir", value=source_dir, expected_type=type_hints["source_dir"])
            check_type(argname="argument source_file", value=source_file, expected_type=type_hints["source_file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "output_path": output_path,
            "type": type,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if excludes is not None:
            self._values["excludes"] = excludes
        if exclude_symlink_directories is not None:
            self._values["exclude_symlink_directories"] = exclude_symlink_directories
        if output_file_mode is not None:
            self._values["output_file_mode"] = output_file_mode
        if source is not None:
            self._values["source"] = source
        if source_content is not None:
            self._values["source_content"] = source_content
        if source_content_filename is not None:
            self._values["source_content_filename"] = source_content_filename
        if source_dir is not None:
            self._values["source_dir"] = source_dir
        if source_file is not None:
            self._values["source_file"] = source_file

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def output_path(self) -> builtins.str:
        '''The output of the archive file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#output_path DataArchiveFile#output_path}
        '''
        result = self._values.get("output_path")
        assert result is not None, "Required property 'output_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of archive to generate. NOTE: ``zip`` and ``tar.gz`` is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#type DataArchiveFile#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify files/directories to ignore when reading the ``source_dir``. Supports glob file matching patterns including doublestar/globstar (``**``) patterns.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#excludes DataArchiveFile#excludes}
        '''
        result = self._values.get("excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def exclude_symlink_directories(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Boolean flag indicating whether symbolically linked directories should be excluded during the creation of the archive. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#exclude_symlink_directories DataArchiveFile#exclude_symlink_directories}
        '''
        result = self._values.get("exclude_symlink_directories")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def output_file_mode(self) -> typing.Optional[builtins.str]:
        '''String that specifies the octal file mode for all archived files.

        For example: ``"0666"``. Setting this will ensure that cross platform usage of this module will not vary the modes of archived files (and ultimately checksums) resulting in more deterministic behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#output_file_mode DataArchiveFile#output_file_mode}
        '''
        result = self._values.get("output_file_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataArchiveFileSource"]]]:
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#source DataArchiveFile#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataArchiveFileSource"]]], result)

    @builtins.property
    def source_content(self) -> typing.Optional[builtins.str]:
        '''Add only this content to the archive with ``source_content_filename`` as the filename.

        One and only one of ``source``, ``source_content_filename`` (with ``source_content``), ``source_file``, or ``source_dir`` must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#source_content DataArchiveFile#source_content}
        '''
        result = self._values.get("source_content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_content_filename(self) -> typing.Optional[builtins.str]:
        '''Set this as the filename when using ``source_content``.

        One and only one of ``source``, ``source_content_filename`` (with ``source_content``), ``source_file``, or ``source_dir`` must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#source_content_filename DataArchiveFile#source_content_filename}
        '''
        result = self._values.get("source_content_filename")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_dir(self) -> typing.Optional[builtins.str]:
        '''Package entire contents of this directory into the archive.

        One and only one of ``source``, ``source_content_filename`` (with ``source_content``), ``source_file``, or ``source_dir`` must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#source_dir DataArchiveFile#source_dir}
        '''
        result = self._values.get("source_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_file(self) -> typing.Optional[builtins.str]:
        '''Package this file into the archive.

        One and only one of ``source``, ``source_content_filename`` (with ``source_content``), ``source_file``, or ``source_dir`` must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#source_file DataArchiveFile#source_file}
        '''
        result = self._values.get("source_file")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataArchiveFileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-archive.dataArchiveFile.DataArchiveFileSource",
    jsii_struct_bases=[],
    name_mapping={"content": "content", "filename": "filename"},
)
class DataArchiveFileSource:
    def __init__(self, *, content: builtins.str, filename: builtins.str) -> None:
        '''
        :param content: Add this content to the archive with ``filename`` as the filename. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#content DataArchiveFile#content}
        :param filename: Set this as the filename when declaring a ``source``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#filename DataArchiveFile#filename}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5904c5461679cf6f1f619fb8bf2ab9cf44afa5adb738fa7a85022f5f3df3fa5b)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "filename": filename,
        }

    @builtins.property
    def content(self) -> builtins.str:
        '''Add this content to the archive with ``filename`` as the filename.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#content DataArchiveFile#content}
        '''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filename(self) -> builtins.str:
        '''Set this as the filename when declaring a ``source``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/archive/2.7.0/docs/data-sources/file#filename DataArchiveFile#filename}
        '''
        result = self._values.get("filename")
        assert result is not None, "Required property 'filename' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataArchiveFileSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataArchiveFileSourceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-archive.dataArchiveFile.DataArchiveFileSourceList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88a478b72b8e8d3138dbcc97340cac916ce14a6ffea6dcc31af91669013d567f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataArchiveFileSourceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3db9d94aea08c3bdc2cca23e3649df8e1c5463390f53f0bbbcede6dee2eac5d8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataArchiveFileSourceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d969f8d3a7e5efbd20dff84d65fa9b0b38f7d611603684a884c5428bea6fc2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a03dc94d13173c2918de795b846220520d863e45e28a2261aba13df1c3ce1be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b28112c47e238306e0bab024eb02c6bb5507f1a3c32e6e8989594831c5ae16f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataArchiveFileSource]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataArchiveFileSource]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataArchiveFileSource]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d17689ad2b65c75353ee71da6eb42a0dc15d46d1bb15a55d37262a6c529abb45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataArchiveFileSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-archive.dataArchiveFile.DataArchiveFileSourceOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__104762102aeec1438fe2a86c64c84c2f5a8a4a5cbdf8451e8b6ecdda38d0394d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="filenameInput")
    def filename_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filenameInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31aec45310cdcf623c915cf360d129eae107e050394d784d0d9359096924d572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filename")
    def filename(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filename"))

    @filename.setter
    def filename(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbbf017c25c7cdf0d4de3e08d2ef9b67870fe102ed7e2403c21a798c5c1bfb6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filename", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataArchiveFileSource]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataArchiveFileSource]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataArchiveFileSource]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fc6924f9fc21231348b7a9b6caf4050cbb99f5ab9bdcb76e627f9583bcc0a6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataArchiveFile",
    "DataArchiveFileConfig",
    "DataArchiveFileSource",
    "DataArchiveFileSourceList",
    "DataArchiveFileSourceOutputReference",
]

publication.publish()

def _typecheckingstub__3f8174f229f3604133f5c77a80cd25d2977aef1687fff32139249b73dce43cf7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    output_path: builtins.str,
    type: builtins.str,
    excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    exclude_symlink_directories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    output_file_mode: typing.Optional[builtins.str] = None,
    source: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataArchiveFileSource, typing.Dict[builtins.str, typing.Any]]]]] = None,
    source_content: typing.Optional[builtins.str] = None,
    source_content_filename: typing.Optional[builtins.str] = None,
    source_dir: typing.Optional[builtins.str] = None,
    source_file: typing.Optional[builtins.str] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__469ab24a096cafd72d07fc9c3aa875004cf4af1d04e6d0ba5bb367da90840577(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d003f85638c28bffbd4441abb65c0dc94b23f40ab53f06c48a8d24b28d5f42be(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataArchiveFileSource, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20c4285397b574ace2586d5b7d9c0efed97c37db7016848d04cb03aa64878453(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63461d561599bf3138af7b713358f4ca8a37731df554faa092adba7988d201e6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cf0d3fbf6707bec587f4a960cd54edd8e60f917d78b8b942cc183e29c7291d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3592643f4a565fac9e7ff8c5189ac2f818943f620f705989325f0070d0f74749(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4f7f1c2a67ef2d6cd3380e72c2663d13a07e8a175ff5a4cf7f68c4df802c472(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ddff38facb63d2db815fde82cff0e0559b482fd07b09a7c023eac38911966c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9dfe185d1160c0d01df7661702ee3e6ce0223ba9ffbf6fe85f7c82315c1702f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb49ee8a8a77e542ce50503f7116ae685411f0a635d0e39bb93fc1d4c370ceb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60c0778b3789354f6804e1c1ce39630da6b9932c71223ea45e1bb6b723916262(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__395d6c956a8f6a157e1bf9db0b880a72f8d80755220480442d2acbff968ca74f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    output_path: builtins.str,
    type: builtins.str,
    excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    exclude_symlink_directories: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    output_file_mode: typing.Optional[builtins.str] = None,
    source: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataArchiveFileSource, typing.Dict[builtins.str, typing.Any]]]]] = None,
    source_content: typing.Optional[builtins.str] = None,
    source_content_filename: typing.Optional[builtins.str] = None,
    source_dir: typing.Optional[builtins.str] = None,
    source_file: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5904c5461679cf6f1f619fb8bf2ab9cf44afa5adb738fa7a85022f5f3df3fa5b(
    *,
    content: builtins.str,
    filename: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a478b72b8e8d3138dbcc97340cac916ce14a6ffea6dcc31af91669013d567f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db9d94aea08c3bdc2cca23e3649df8e1c5463390f53f0bbbcede6dee2eac5d8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d969f8d3a7e5efbd20dff84d65fa9b0b38f7d611603684a884c5428bea6fc2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a03dc94d13173c2918de795b846220520d863e45e28a2261aba13df1c3ce1be(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b28112c47e238306e0bab024eb02c6bb5507f1a3c32e6e8989594831c5ae16f2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d17689ad2b65c75353ee71da6eb42a0dc15d46d1bb15a55d37262a6c529abb45(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataArchiveFileSource]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__104762102aeec1438fe2a86c64c84c2f5a8a4a5cbdf8451e8b6ecdda38d0394d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31aec45310cdcf623c915cf360d129eae107e050394d784d0d9359096924d572(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbbf017c25c7cdf0d4de3e08d2ef9b67870fe102ed7e2403c21a798c5c1bfb6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc6924f9fc21231348b7a9b6caf4050cbb99f5ab9bdcb76e627f9583bcc0a6a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataArchiveFileSource]],
) -> None:
    """Type checking stubs"""
    pass
