from pytest import approx


def test_static_maker(mock_vasp, clean_dir, si_structure):
    from jobflow import run_locally

    from atomate2.vasp.jobs.core import StaticMaker
    from atomate2.vasp.schemas.task import TaskDocument

    # mapping from job name to directory containing test files
    ref_paths = {"static": "Si_band_structure/static"}

    # settings passed to fake_run_vasp; adjust these to check for certain INCAR settings
    fake_run_vasp_kwargs = {"static": {"incar_settings": ["NSW", "ISMEAR"]}}

    # automatically use fake VASP and write POTCAR.spec during the test
    mock_vasp(ref_paths, fake_run_vasp_kwargs)

    # generate job
    job = StaticMaker().make(si_structure)

    # run the flow or job and ensure that it finished running successfully
    responses = run_locally(job, create_folders=True, ensure_success=True)

    # validation the outputs of the job
    output1 = responses[job.uuid][1].output
    assert isinstance(output1, TaskDocument)
    assert output1.output.energy == approx(-10.85037078)


def test_relax_maker(mock_vasp, clean_dir, si_structure):
    from jobflow import run_locally

    from atomate2.vasp.jobs.core import RelaxMaker
    from atomate2.vasp.schemas.task import TaskDocument

    # mapping from job name to directory containing test files
    ref_paths = {"relax": "Si_double_relax/relax_1"}

    # settings passed to fake_run_vasp; adjust these to check for certain INCAR settings
    fake_run_vasp_kwargs = {"relax": {"incar_settings": ["NSW", "ISMEAR"]}}

    # automatically use fake VASP and write POTCAR.spec during the test
    mock_vasp(ref_paths, fake_run_vasp_kwargs)

    # generate job
    job = RelaxMaker().make(si_structure)

    # run the flow or job and ensure that it finished running successfully
    responses = run_locally(job, create_folders=True, ensure_success=True)

    # validation the outputs of the job
    output1 = responses[job.uuid][1].output
    assert isinstance(output1, TaskDocument)
    assert output1.output.energy == approx(-10.85083141)
    assert len(output1.calcs_reversed[0].output.ionic_steps) == 1
    assert output1.input.parameters["NSW"] > 1


def test_dielectric(mock_vasp, clean_dir, si_structure):
    import numpy as np
    from jobflow import run_locally

    from atomate2.vasp.jobs.core import DielectricMaker

    # mapping from job name to directory containing test files
    ref_paths = {"dielectric": "Si_dielectric"}

    # settings passed to fake_run_vasp; adjust these to check for certain INCAR settings
    fake_run_vasp_kwargs = {"dielectric": {"incar_settings": ["NSW", "IBRION"]}}

    # automatically use fake VASP and write POTCAR.spec during the test
    mock_vasp(ref_paths, fake_run_vasp_kwargs)

    # Generate dielectric flow
    job = DielectricMaker().make(si_structure)
    job.maker.input_set_generator.user_incar_settings["KSPACING"] = 0.5

    # Run the flow or job and ensure that it finished running successfully
    responses = run_locally(job, create_folders=True, ensure_success=True)

    # Additional validation on the outputs of the job
    output1 = responses[job.uuid][1].output
    assert np.allclose(
        output1.calcs_reversed[0].output.epsilon_static,
        [[11.41539467, 0, 0], [0, 11.41539963, 0], [0, 0, 11.41539866]],
        atol=0.01,
    )
    assert np.allclose(
        output1.calcs_reversed[0].output.epsilon_ionic,
        [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        atol=0.01,
    )


def test_hse_relax(mock_vasp, clean_dir, si_structure):
    from jobflow import run_locally

    from atomate2.vasp.jobs.core import HSERelaxMaker
    from atomate2.vasp.schemas.task import TaskDocument

    # mapping from job name to directory containing test files
    ref_paths = {"hse relax": "Si_hse_relax"}

    # settings passed to fake_run_vasp; adjust these to check for certain INCAR settings
    fake_run_vasp_kwargs = {"hse relax": {"incar_settings": ["NSW", "ISMEAR"]}}

    # automatically use fake VASP and write POTCAR.spec during the test
    mock_vasp(ref_paths, fake_run_vasp_kwargs)

    # generate job
    job = HSERelaxMaker().make(si_structure)
    job.maker.input_set_generator.user_incar_settings["KSPACING"] = 0.4

    # Run the job and ensure that it finished running successfully
    responses = run_locally(job, create_folders=True, ensure_success=True)

    # validation on the output of the job
    output1 = responses[job.uuid][1].output
    assert isinstance(output1, TaskDocument)
    assert output1.output.energy == approx(-12.5326576)
    assert len(output1.calcs_reversed[0].output.ionic_steps) == 3
    assert output1.input.parameters["NSW"] > 1


def test_static_maker(mock_vasp, clean_dir, si_structure):
    from jobflow import run_locally

    from atomate2.vasp.jobs.core import HSEStaticMaker
    from atomate2.vasp.schemas.task import TaskDocument

    # mapping from job name to directory containing test files
    ref_paths = {"hse static": "Si_hse_band_structure/hse_static"}

    # settings passed to fake_run_vasp; adjust these to check for certain INCAR settings
    fake_run_vasp_kwargs = {"hse static": {"incar_settings": ["NSW", "ISMEAR"]}}

    # automatically use fake VASP and write POTCAR.spec during the test
    mock_vasp(ref_paths, fake_run_vasp_kwargs)

    # generate job
    job = HSEStaticMaker().make(si_structure)
    job.maker.input_set_generator.user_incar_settings["KSPACING"] = 0.4

    # run the flow or job and ensure that it finished running successfully
    responses = run_locally(job, create_folders=True, ensure_success=True)

    # validation the outputs of the job
    output1 = responses[job.uuid][1].output
    assert isinstance(output1, TaskDocument)
    assert output1.output.energy == approx(-12.52887403)